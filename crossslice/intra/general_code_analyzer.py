import copy
import json
import re
import traceback
import uuid
import os
import sys
from typing import Dict, Set, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, field
from tree_sitter import Node

# Add the project root to Python path

from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC

#
# ────────────────────────────────────────────────────────────────────────────────
#  0. Languages: Language specific imports/definitions
# ────────────────────────────────────────────────────────────────────────────────
#
C_TOP_LEVEL_TYPES = [
    "linkage_specification",
    "declaration",
    "attributed_statement",
    "type_definition",
    "_empty_declaration",
    "preproc_if",
    "preproc_ifdef",
    "preproc_include",
    "preproc_def",
    "preproc_function_def",
    "preproc_call",
    "struct_specifier",
    "union_specifier",
    "enum_specifier",
    "macro_type_specifier",
    "sized_type_specifier",
    "primitive_type",
    "_type_identifier",
]

# Multi-line structures that can benefit from partial showing
C_MULTILINE_STRUCTURES = {
    "struct_specifier": {"threshold": 20, "show_context": True},
    "union_specifier": {"threshold": 15, "show_context": True}, 
    "enum_specifier": {"threshold": 15, "show_context": True},
    "preproc_if": {"threshold": 30, "show_context": True},
    "preproc_ifdef": {"threshold": 30, "show_context": True},
    "linkage_specification": {"threshold": 25, "show_context": True}
}

#
# ────────────────────────────────────────────────────────────────────────────────
#  0.1. Global Context Functions
# ────────────────────────────────────────────────────────────────────────────────
#
def remove_function_definitions_from_node(node):
    """
    Create a modified version of the node that excludes any function definitions.
    For preprocessor directives, this keeps the directive but removes function definitions inside.
    Returns None if the node itself is a function definition.
    """
    if node.type == "function_definition":
        print("=" * 50)
        print("=" * 50)
        return None
    
    # For nodes that might contain function definitions, we need to filter their children
    if hasattr(node, 'named_children') and node.named_children:
        # Create a new node-like object with filtered children
        class FilteredNode:
            def __init__(self, original_node):
                self.type = original_node.type
                self.start_point = original_node.start_point
                self.end_point = original_node.end_point
                self.text = original_node.text
                self.id = getattr(original_node, 'id', None)
                self.parent = getattr(original_node, 'parent', None)
                self.start_byte = original_node.start_byte
                self.end_byte = original_node.end_byte
                
                # Filter out function definitions from children
                self.named_children = []
                for child in original_node.named_children:
                    filtered_child = remove_function_definitions_from_node(child)
                    if filtered_child is not None:
                        self.named_children.append(filtered_child)
        
        return FilteredNode(node)
    else:
        # Leaf node or node without children - return as is
        return node

class FilteredNode:
    """
    Wrapper around a tree_sitter.Node that:
     - proxies almost all attributes/methods to the original node
     - OVERRIDES .children, .child(), .child_by_field_name(),
       .walk() and .descendants to filter out any
       function_definition subtrees
    """
    __slots__ = ('_node',)
    def __init__(self, node: Node):
        self._node = node

    # — proxy basic read-only props —
    @property
    def type(self):           return self._node.type
    @property
    def start_byte(self):     return self._node.start_byte
    @property
    def end_byte(self):       return self._node.end_byte
    @property
    def start_point(self):    return self._node.start_point
    @property
    def end_point(self):      return self._node.end_point

    # — filtered children list —
    @property
    def children(self):
        return [
            FilteredNode(c)
            for c in self._node.children
            if c.type != 'function_definition'
        ]

    # — filtered single‐child accessors —
    def child(self, i):
        return self.children[i]
    def child_by_field_name(self, name):
        c = self._node.child_by_field_name(name)
        if c is None or c.type == 'function_definition':
            return None
        return FilteredNode(c)

    # — filtered pre‐order walk (yields FilteredNode) —
    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    # — filtered descendants (yields FilteredNode, excludes self) —
    @property
    def descendants(self):
        for c in self.children:
            yield c
            yield from c.descendants

    # — make iteration / len() work the same as .children —
    def __iter__(self):
        return iter(self.children)
    def __len__(self):
        return len(self.children)

    # — everything else falls back to the original Node —
    def __getattr__(self, attr):
        return getattr(self._node, attr)

def filter_function_definitions_tree(root: Node) -> FilteredNode:
    """
    Wrap the given tree-sitter root node in a FilteredNode
    that omits all function_definition subtrees.
    """
    if root.type == 'function_definition':
        return None
    return FilteredNode(root)

def ast_to_code(node: FilteredNode, src: bytes, strip_comments: bool = True) -> str:
    """
    Reconstruct the exact bytes of `src` covered by `node`, *minus*
    any function_definition subtrees and optionally comments.

    Args:
        node: The FilteredNode to convert to code
        src: The source code bytes
        strip_comments: If True, remove comment nodes from the output (default: True)
    """
    orig = node._node

    # 1) collect all spans to remove (function_definitions and optionally comments)
    spans_to_remove = []
    def collect(n):
        if n.type == 'function_definition':
            spans_to_remove.append((n.start_byte, n.end_byte))
        elif strip_comments and n.type == 'comment':
            spans_to_remove.append((n.start_byte, n.end_byte))
        for c in n.children:
            collect(c)
    collect(orig)

    # if there’s nothing to remove, just slice once
    if not spans_to_remove:
        return src[orig.start_byte : orig.end_byte].decode()

    # 2) merge overlapping/adjacent spans
    spans_to_remove.sort()
    merged = []
    for s, e in spans_to_remove:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # 3) walk through [orig.start_byte, orig.end_byte), cutting out the merged spans
    parts = []
    cursor = orig.start_byte
    for s, e in merged:
        # skip anything entirely outside our node’s range
        if e <= orig.start_byte or s >= orig.end_byte:
            continue
        # clamp to this node’s slice
        s_clamped = max(s, orig.start_byte)
        e_clamped = min(e, orig.end_byte)

        # append everything up to the removed span
        if cursor < s_clamped:
            parts.append(src[cursor : s_clamped])
        # skip the span
        cursor = e_clamped

    # append any trailing bytes
    if cursor < orig.end_byte:
        parts.append(src[cursor : orig.end_byte])

    return b''.join(parts).decode()

def get_top_level_nodes(root_node):
    """
    Extract all top-level nodes from the C AST root that are relevant for global context.
    For nodes that contain function definitions, removes those function definitions
    while keeping the rest of the node structure.
    """
    top_level_nodes = []
    for child in root_node.named_children:
        if child.type in C_TOP_LEVEL_TYPES:
            # Filter out function definitions from within the node
            filtered_node = remove_function_definitions_from_node(child)
            if filtered_node is not None:
                top_level_nodes.append(filtered_node)
    return top_level_nodes

def intersects_with_changes(node, changed_lines):
    """
    Check if a node intersects with changed lines (with context window).

    Lines have to be 0-based!
    """
    if not changed_lines:
        return False
        
    node_start = node.start_point[0]  # 0-based
    node_end = node.end_point[0]      # 0-based
    
    # Check if node overlaps with changed lines + context
    for changed_line in changed_lines:
        if (node_start <= changed_line and node_end >= changed_line):
            return True
    return False

def should_show_partial_structure(node):
    """
    Determine if a multi-line structure should be shown partially or entirely.
    """
    if node.type not in C_MULTILINE_STRUCTURES:
        return False, False  # show_partial=False, show_context=False
    
    config = C_MULTILINE_STRUCTURES[node.type]
    node_lines = node.end_point[0] - node.start_point[0] + 1
    
    if node_lines > config["threshold"]:
        return True, config["show_context"]  # show_partial=True
    else:
        return False, False  # show_partial=False, show entire structure

#
# ────────────────────────────────────────────────────────────────────────────────
#  1. Utilities: JSON loading and simple cleaning
# ────────────────────────────────────────────────────────────────────────────────
#
def load_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
ctf_mapping = load_json(os.path.join(_DATA_DIR, "control_flow_mapping_c.json"))
field_role_map = load_json(os.path.join(_DATA_DIR, "field_mapping_c.json"))
    
def clean_string(text: bytes) -> str:
    """
    Clean the text from unwanted characters
    """
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)
    # Remove spaces before commas
    text = re.sub(r'\s+,', ',', text)
    # Remove spaces before and after parentheses
    text = re.sub(r'\s*\(\s*', '(', text)  # Space before and after '('
    text = re.sub(r'\s*\)\s*', ')', text)  # Space before and after ')'
    # Ensure there's exactly one space after commas
    text = re.sub(r',\s*', ', ', text)
    # Remove space between type keywords and identifiers (optional, generic cleanup)
    text = re.sub(r'\b\s+', ' ', text)  # Fix spaces after types like "double" or "int"
    return text.strip()

def get_node_text_without_comments(node) -> str:
    """
    Get the text of a tree-sitter node with all comment nodes removed.
    This is useful when comparing expressions to detect actual code changes
    vs comment-only changes.

    Args:
        node: A tree-sitter node

    Returns:
        The node's text with all comment content removed
    """
    # Get the raw bytes of this node
    node_bytes = node.text
    node_start = node.start_byte

    # Collect all comment spans within this node
    comment_spans = []

    def collect_comments(n):
        if n.type == 'comment':
            # Store relative positions within the node
            rel_start = n.start_byte - node_start
            rel_end = n.end_byte - node_start
            comment_spans.append((rel_start, rel_end))
        for child in n.children:
            collect_comments(child)

    collect_comments(node)

    # If no comments, return the original text
    if not comment_spans:
        return node_bytes.decode("utf-8")

    # Sort and merge overlapping spans
    comment_spans.sort()
    merged = []
    for s, e in comment_spans:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # Build the result by excluding comment spans
    parts = []
    cursor = 0
    for s, e in merged:
        if s > cursor:
            parts.append(node_bytes[cursor:s])
        cursor = e

    # Append anything after the last comment
    if cursor < len(node_bytes):
        parts.append(node_bytes[cursor:])

    return b''.join(parts).decode("utf-8")

def convert_to_json_compatible(data):
    """
    Recursively convert all sets and non-JSON serializable elements in the result to JSON-compatible types.
    """
    if isinstance(data, dict):
        return {key: convert_to_json_compatible(value) for key, value in data.items()}
    elif isinstance(data, set):
        return list(data)  # Convert sets to lists
    elif isinstance(data, list):
        return [convert_to_json_compatible(item) for item in data]
    else:
        return data

def is_valid_argument_node(node):
    """
    Check if a node is a valid argument (exclude symbols like ',' or '(').
    """
    # tree-sitter puts unknown trailing tokens (`x TSRMLS_CC`, attribute macros)
    # into an ERROR child; it is not an argument and must not count as one
    return node.type not in {',', '(', ')', 'ERROR', 'comment'}

def is_compound_assignment(node):
    # Tree-sitter stores the operator text in node.child_by_field_name("operator")
    op = node.child_by_field_name("operator")
    if op:
        text = op.text.decode("utf-8")
        return text.endswith("=") and text != "="
    return False

# ---------------------------------------------------------------------------
# Helper utilities for robust parameter extraction (added)
# ---------------------------------------------------------------------------
def _find_identifier_descendant(node):
    """Return first descendant whose type == 'identifier'."""
    if node is None:
        return None
    if node.type == 'identifier':
        return node
    stack = list(getattr(node, 'named_children', []))
    while stack:
        cur = stack.pop()
        if cur.type == 'identifier':
            return cur
        stack.extend(getattr(cur, 'named_children', []))
    return None

def extract_parameter_identifiers(parameters_node):
    """Return list of (name, id_node) for each parameter in a parameter_list.
    Handles pointer_declarator / array_declarator chains etc.
    """
    out = []
    if not parameters_node:
        return out
    for p in parameters_node.children:
        if p.type != 'parameter_declaration':
            continue
        decl = p.child_by_field_name('declarator')
        id_node = _find_identifier_descendant(decl)
        if id_node is not None:
            out.append((id_node.text.decode('utf-8'), id_node))
    return out

#
# ────────────────────────────────────────────────────────────────────────────────
#  2. Scope Manager & Variable Classes (with integer IDs + depth)
# ────────────────────────────────────────────────────────────────────────────────
#
class Variable:
    """
    Represents a single variable instance (unique by declaration).
    """
    def __init__(self, name: str, scope_id: int, defining_node_id: int):
        self.name = name
        self.scope_id = scope_id
        self.defining_node_id = defining_node_id
        self.id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "var_id":   self.id,
            "name":     self.name,
            "scope_id": self.scope_id
        }
    
class Scope:
    """
    A single lexical scope, with:
      • scope_id    : small integer (1,2,3,…)
      • depth       : 1 = function-level; 2 = one block deeper; etc.
      • parent      : the enclosing Scope or None
      • node_id     : the AST node.id (compound or function) that created this scope
      • variables   : dict name→Variable
    """
    def __init__(self, parent_scope: 'Scope' = None, node_id: int = None, scope_id: int = None):
        self.parent = parent_scope
        self.node_id = node_id
        self.scope_id = scope_id
        self.depth = 1 if parent_scope is None else parent_scope.depth + 1
        self.variables = {}  # name → Variable

    def declare_variable(self, var: Variable):
        # If the same name appears again in this scope, it shadows. That’s fine.
        self.variables[var.name] = var

    def resolve_name(self, name: str) -> Variable:
        """
        Look up “name” in this scope; if not found, recurse into parent.
        """
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.resolve_name(name)
        return None
    
class ScopeManager:
    """
    Manages a stack of open scopes and maps AST node.id → Scope instance.
    Assigns each new scope a small integer ID (1,2,3,…).
    """
    def __init__(self):
        # create global scope with scope_id = 0
        global_scope = Scope(parent_scope=None, node_id=0, scope_id=0)
        global_scope.depth = 0
        self.global_scope = global_scope

        # init so that current_scope start at global
        self.current_scope = global_scope
        self.scopes_by_node_id = {0: global_scope}  # node.id → Scope

        self.next_scope_id = 1

    def enter_scope(self, node_id: int) -> Scope:
        """
        Called when entering a new `compound_statement` or function body.
        Creates a new Scope with:
          - scope_id = next integer,
          - depth = parent.depth + 1 (or 1 if no parent).
        """
        parent = self.current_scope
        sid = self.next_scope_id
        self.next_scope_id += 1
        new_scope = Scope(parent_scope=parent, node_id=node_id, scope_id=sid)
        self.current_scope = new_scope
        self.scopes_by_node_id[node_id] = new_scope
        return new_scope

    def exit_scope(self):
        """
        Pop one scope (when leaving a compound_statement).
        """
        if self.current_scope:
            self.current_scope = self.current_scope.parent

    def declare(self, name: str, node_id: int) -> Variable:
        """
        Register a new Variable(name) in the CURRENT scope (using that scope’s integer ID).
        """
        if not self.current_scope:
            raise RuntimeError("Declaring a variable with no current scope!")
        var = Variable(name=name, scope_id=self.current_scope.scope_id, defining_node_id=node_id)
        self.current_scope.declare_variable(var)
        return var
    
    def declare_global(self, name: str, defining_node_id: int) -> Variable:
        """
        If `name` not yet in global scope, create it there.
        Always return the single Variable instance for that name.
        """
        if name in self.global_scope.variables:
            return self.global_scope.variables[name]
        var = Variable(name=name, scope_id=self.global_scope.scope_id, defining_node_id=defining_node_id)
        self.global_scope.declare_variable(var)
        return var

    def resolve(self, name: str, starting_scope: Scope) -> Variable:
        """
        Starting from `starting_scope`, walk up until we find a Variable with this name.
        Return None if not found.
        """
        return starting_scope.resolve_name(name) if starting_scope else None

    def resolve_any(self, name: str) -> Optional[Variable]:
        """Fallback: search all known scopes (prefer deepest depth) for a variable name.
        Deepest = most shadowed; this better emulates lexical lookup if caller
        failed to supply the correct starting scope.
        """
        found = []
        for scope in self.scopes_by_node_id.values():
            if name in scope.variables:
                found.append((scope.depth, scope.variables[name]))
        if not found:
            return None
        # prefer largest depth (most specific / innermost scope)
        found.sort(key=lambda item: -item[0])
        return found[0][1]

    def get_scope_for_node(self, node, fallback: Scope = None) -> Scope:
        """
        Climb ancestors looking for a compound_statement whose node.id is in scopes_by_node_id.
        If found, return that Scope. Otherwise, return fallback.
        """
        cur = node

        # if not isinstance(cur, Node):
        #     print("Warning: get_scope_for_node called with non-Node object!")
        #     print("Node type:", type(cur))
        #     print("node:", cur)

        while cur is not None:
            if cur.type == "compound_statement" and cur.id in self.scopes_by_node_id:
                return self.scopes_by_node_id[cur.id]
            cur = cur.parent
        return fallback
        
    def print_state(self):
        """
        Print the current state of the ScopeManager: for each scope, display its
        scope_id, depth, node_id, parent scope_id, and all declared variables.
        """
        scopes = sorted(self.scopes_by_node_id.values(), key=lambda s: s.scope_id)
        for scope in scopes:
            parent_id = scope.parent.scope_id if scope.parent else None
            print(f"Scope {scope.scope_id} (depth={scope.depth}, node_id={scope.node_id}, parent={parent_id})")
            if scope.variables:
                for var_name, var in scope.variables.items():
                    print(f"  Variable: {var_name} (id={var.id}, defined at node {var.defining_node_id})")
            else:
                print("  No variables declared in this scope.")
            print("-" * 40)
    
#
# ────────────────────────────────────────────────────────────────────────────────
#  3. register_declarations
# ────────────────────────────────────────────────────────────────────────────────
#
def register_declarations(node, scope_manager):
    """
    Recursively walk the AST under `node`. Whenever we see:
      • A compound_statement → enter a new scope (node.id), recurse, then exit.
      • Any node with child_by_field_name("declarator") → find its inner identifier and declare it.
      • Any `identifier` whose parent is `parameter_declaration` → declare it.

    Otherwise, just recurse. This builds the complete scope/variable map for the function.
    """
    # 1) If it’s a compound_statement, open a new scope:
    if node.type == "compound_statement":
        scope_manager.enter_scope(node.id)
        for child in node.named_children:
            register_declarations(child, scope_manager)
        scope_manager.exit_scope()
        return

    # 2) If this node has a `declarator` field, that subtree introduces a new variable:
    decl_child = node.child_by_field_name("declarator")
    if decl_child:
        # Find the first `identifier` descendant in the declarator
        id_node = None
        
        # Special handling for init_declarator: only look in its declarator field
        if decl_child.type == "init_declarator":
            actual_declarator = decl_child.child_by_field_name("declarator")
            if actual_declarator:
                if actual_declarator.type == "identifier":
                    id_node = actual_declarator
                else:
                    stack = [actual_declarator]
                    while stack and id_node is None:
                        cur = stack.pop()
                        if cur.type == "identifier":
                            id_node = cur
                            break
                        stack.extend(cur.named_children)
        else:
            # Regular declarator handling
            if decl_child.type == "identifier":
                id_node = decl_child
            else:
                stack = [decl_child]
                while stack and id_node is None:
                    cur = stack.pop()
                    if cur.type == "identifier":
                        id_node = cur
                        break
                    stack.extend(cur.named_children)

        if id_node:
            name = id_node.text.decode("utf-8")
            scope_manager.declare(name, id_node.id)

        # Only recurse into the declarator itself, not the entire declaration
        # This prevents processing initializers as declarations
        register_declarations(decl_child, scope_manager)
        return

    # 2.1) Special case: init_declarator - only process the declarator, skip the initializer
    if node.type == "init_declarator":
        declarator = node.child_by_field_name("declarator")
        if declarator:
            register_declarations(declarator, scope_manager)
        # Do NOT recurse into other children (which includes the initializer)
        return

    # 3) If this node is an `identifier` inside a `parameter_declaration`, declare it:
    if node.type == "identifier" and node.parent and node.parent.type == "parameter_declaration":
        # print(node)
        name = node.text.decode("utf-8")
        scope_manager.declare(name, node.id)
        return

    # 4) Otherwise, recurse into children:
    for child in node.named_children:
        register_declarations(child, scope_manager)

#
# ────────────────────────────────────────────────────────────────────────────────
#  4. collect_statements (flatten)
# ────────────────────────────────────────────────────────────────────────────────
#
def collect_statements(node, statement_types, out_list):
    """
    Recursively traverse `node`. Whenever node.type is in statement_types,
    append it to out_list and continue descending to catch nested statements.
    Otherwise, keep recursing until we find a statement.
    """
    if node.type in statement_types:
        out_list.append(node)
        for child in node.named_children:
            collect_statements(child, statement_types, out_list)
    else:
        for child in node.named_children:
            collect_statements(child, statement_types, out_list)

#
# ────────────────────────────────────────────────────────────────────────────────
#  5. walk_defs_uses_scalar (the scalar engine, kept) and walk_defs_uses (entry point)
# ────────────────────────────────────────────────────────────────────────────────
#
def walk_defs_uses_scalar(node, field_role_map, defs_out, uses_out, role="use", scope_manager: ScopeManager = None, 
                   stmt_scope: Scope = None, call_role_map: dict = None, id_type_str: str = "variable"):
    """
    The scalar engine (kept for reference and for `CROSSSLICE_DEFUSE=scalar`; not
    called otherwise — `walk_defs_uses` below delegates to the field-sensitive
    engine in access_paths.py).

    Recursively walk AST under `node`. Every time we hit an `identifier`:
        - Resolve via stmt_scope
        - Record it in defs_out (if role=="def") or uses_out (if role=="use)

    Use field_role_map in general to split child-fields into "def" vs. "use".
    If node.type == "call_expression":
        - Extract called function name
        - Look up in call_role_map if function is input function (e.g., "printf") --> 
          if so, treat all its arguments as "definitions" (e.g., printf("%s", var))
    """
    # 1) If identifier, record it:
    if node.type == "identifier":
        name = node.text.decode("utf-8")
        sr, sc = node.start_point
        er, ec = node.end_point

        # try to resilve in curretn function scope chain
        resolved_var = None
        if scope_manager and stmt_scope:
            resolved_var = scope_manager.resolve(name, stmt_scope)

        # fallback: maybe declared in another ancestor scope we missed
        if resolved_var is None and scope_manager:
            resolved_var = scope_manager.resolve_any(name)

        # if not found, declare/use it as global
        if resolved_var is None:
            # If role was 'def' but we can't find an existing declaration, treat it as a use of an external/global
            # and then create a single global instance so all later uses share it.
            resolved_var = scope_manager.declare_global(name, node.id)

        # determine identifier kind
        id_type = id_type_str

        entry = {
            "name": name,
            "position_start": [sr, sc],
            "position_end": [er, ec],
            "var_id": resolved_var.id,
            "scope_id": resolved_var.scope_id,
            "id_type": id_type,
        }

        # Avoid class/struct member and pointer member fields being treated as definitions
        parent_type = node.parent.type if getattr(node, 'parent', None) else None
        if role == 'def' and parent_type in { 'field_expression', 'pointer_expression' }:
            role = 'use'

        # Avoid treating member / pointer access base identifiers as new definitions
        parent_type = node.parent.type if getattr(node, 'parent', None) else None
        if role == 'def' and parent_type in { 'field_expression', 'pointer_expression' }:
            role = 'use'

        if role == "def":
            defs_out.append(entry)
        elif role == "use":
            uses_out.append(entry)

        return
    
    # 2) Special case: call_expression
    if node.type == "call_expression" and call_role_map is not None:
        # extract function name
        fn_node = node.child_by_field_name("function")
        func_name = ""
        if fn_node and fn_node.type == "identifier":
            func_name = fn_node.text.decode("utf-8")
        elif fn_node:
            # case of more complex callee (e.g. *(fptr)(arg1, arg2)), just extract text
            func_name = clean_string(fn_node.text.decode("utf-8"))

        # recurse into callee expression as a "use"
        if fn_node:
            walk_defs_uses_scalar(fn_node, field_role_map, defs_out, uses_out, role="use", scope_manager=scope_manager, 
                           stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str="function_call")
            
        # handle arguments list:
        args_node = node.child_by_field_name("arguments")
        if args_node:
            for arg in args_node.children:
                if is_valid_argument_node(arg):
                    # check if this function is in call_role_map
                    if func_name in call_role_map:
                        # if so, treat this argument as a "definition"
                        walk_defs_uses_scalar(arg, field_role_map, defs_out, uses_out, role="def", scope_manager=scope_manager, 
                                       stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str="variable")
                    else:
                        # otherwise, treat it as a "use"
                        walk_defs_uses_scalar(arg, field_role_map, defs_out, uses_out, role="use", scope_manager=scope_manager, 
                                       stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str="variable")
        return

    # 2.1) Special case: compound_assignment
    if node.type == "assignment_expression" and is_compound_assignment(node):
        # For compound assignments, we treate the left side as def and use the right side as use.
        # Find the left side (the variable being assigned to)
        left_node = node.child_by_field_name("left")
        if left_node:
            walk_defs_uses_scalar(left_node, field_role_map, defs_out, uses_out,
                        role="def", scope_manager=scope_manager, stmt_scope=stmt_scope, 
                        call_role_map=call_role_map, id_type_str=id_type_str)
            
            walk_defs_uses_scalar(left_node, field_role_map, defs_out, uses_out,
                        role="use", scope_manager=scope_manager, stmt_scope=stmt_scope, 
                        call_role_map=call_role_map, id_type_str=id_type_str)
            
        # Find the right side (the expression being assigned)
        right_node = node.child_by_field_name("right")
        if right_node:
            walk_defs_uses_scalar(right_node, field_role_map, defs_out, uses_out,
                        role="use", scope_manager=scope_manager, stmt_scope=stmt_scope, 
                        call_role_map=call_role_map, id_type_str=id_type_str)
        return
    
    # 2.2) Special case: if node.type is "return_statement", treat it as a "use" of the return value:
    if node.type == "return_statement":
        # walk all named children of return_statement
        for child in node.named_children:
            walk_defs_uses_scalar(child, field_role_map, defs_out, uses_out,
                           role="use", scope_manager=scope_manager, stmt_scope=stmt_scope,
                           call_role_map=call_role_map, id_type_str=id_type_str)
        return
        
    # 3) If node.type is in field_role_map, split children normally:
    mapping = field_role_map.get(node.type, {})
    if mapping is not None:
        visited = set()

        # Field that define -> "def"
        for field_name in mapping.get("def", []):
            child = node.child_by_field_name(field_name)
            if child:
                visited.add(child.id)
                walk_defs_uses_scalar(child, field_role_map, defs_out, uses_out, role="def", scope_manager=scope_manager, 
                               stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str=id_type_str)
                
        # Field that use -> "use"
        for field_name in mapping.get("use", []):
            child = node.child_by_field_name(field_name)
            if child:
                visited.add(child.id)
                walk_defs_uses_scalar(child, field_role_map, defs_out, uses_out, role="use", scope_manager=scope_manager, 
                               stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str=id_type_str)

        # if this node ias a control flow type, we do not recurse into its other children, so we skip the body
        if node.type in ctf_mapping.get("control_flow_types", []):
            return
             
        # For all other children, recurse normally:
        for child in node.named_children:
            if child.id not in visited:
                walk_defs_uses_scalar(child, field_role_map, defs_out, uses_out, role=role, scope_manager=scope_manager, 
                               stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str=id_type_str)
                
        return
    
    # 4) If no special mapping, just recurse into all named children:
    for child in node.named_children:
        walk_defs_uses_scalar(child, field_role_map, defs_out, uses_out, role=role, scope_manager=scope_manager, 
                       stmt_scope=stmt_scope, call_role_map=call_role_map, id_type_str=id_type_str)


_DEFUSE_ENGINE = os.environ.get("CROSSSLICE_DEFUSE", "fields")   # "fields" | "scalar"


def walk_defs_uses(node, field_role_map, defs_out, uses_out, role="use", scope_manager: ScopeManager = None,
                   stmt_scope: Scope = None, call_role_map: dict = None, id_type_str: str = "variable"):
    """
    Entry point used by analyze_function_ast, analyze_function_ast_global and
    generate_statement_parts. The field-sensitive engine (access_paths.py)
    records the scalar entries plus access-path entries (`s->gb.x`, `len[]`);
    `CROSSSLICE_DEFUSE=scalar` selects the scalar engine above instead.
    """
    if _DEFUSE_ENGINE == "scalar":
        return walk_defs_uses_scalar(node, field_role_map, defs_out, uses_out, role, scope_manager,
                                     stmt_scope, call_role_map, id_type_str)
    from crossslice.intra.access_paths import walk_defs_uses_fields
    return walk_defs_uses_fields(node, field_role_map, defs_out, uses_out, role, scope_manager,
                                 stmt_scope, call_role_map, id_type_str)

#
# ────────────────────────────────────────────────────────────────────────────────
#  6. generate_statement_parts
# ────────────────────────────────────────────────────────────────────────────────
#
def generate_statement_parts(node, field_role_map, parts_map, scope_manager, call_role_map, statement_types):
    """
    Given a control statement node, look up its `parts_map[node.type]`, and for each part:
        - If `part_name` matches a child field, extract that child as a part
        - if `part_name` matches a statement type (e.g. "case_statement"), find all direct
        descendants under the nods body and create one part per such child
        - For preprocessor directives, handle the special structure where content is direct children
    """
    parts = []
    for part_name in parts_map.get(node.type, []):
        candidates = []

        # Handle preprocessor directives specially
        if node.type in ["preproc_if", "preproc_ifdef", "preproc_else", "preproc_elif", "preproc_elifdef"]:
            if part_name == "condition":
                # For preproc_if and preproc_elif, condition is a direct field
                fld_child = node.child_by_field_name("condition")
                if fld_child:
                    candidates.append(fld_child)
            elif part_name == "name":
                # For preproc_ifdef and preproc_elifdef, name is a direct field 
                fld_child = node.child_by_field_name("name")
                if fld_child:
                    candidates.append(fld_child)
            elif part_name == "consequence":
                # For preprocessor directives, the "consequence" is the content between the directive and alternative/endif
                # We need to collect all children that are not condition/name/alternative fields
                consequence_children = []
                alternative_node = node.child_by_field_name("alternative")
                
                # Collect children that are between condition/name and alternative (or end of node)
                start_collecting = False
                for child in node.named_children:
                    if child == node.child_by_field_name("condition") or child == node.child_by_field_name("name"):
                        start_collecting = True
                        continue
                    elif child == alternative_node:
                        break
                    elif start_collecting:
                        consequence_children.append(child)
                
                if consequence_children:
                    # Create a virtual node representing the consequence part
                    if len(consequence_children) == 1:
                        candidates.append(consequence_children[0])
                    else:
                        # For multiple children, we'll handle them as separate statements later
                        # For now, create a virtual part that encompasses all of them
                        first_child = consequence_children[0]
                        last_child = consequence_children[-1]
                        virtual_part = type('VirtualNode', (), {
                            'start_point': first_child.start_point,
                            'end_point': last_child.end_point,
                            'text': b'\n'.join(child.text for child in consequence_children),
                            'named_children': consequence_children,
                            'id': str(uuid.uuid4()),
                            'type': 'virtual_consequence_part',
                            'parent': node,
                        })()
                        candidates.append(virtual_part)
                        
            elif part_name == "alternative":
                # The alternative field contains the else/elif part
                fld_child = node.child_by_field_name("alternative")
                if fld_child:
                    candidates.append(fld_child)
        else:
            # Regular control flow handling
            # direct field
            fld_child = node.child_by_field_name(part_name)
            if fld_child:
                candidates.append(fld_child)
            # statement-type parts under body
            elif part_name in statement_types:
                body = node.child_by_field_name("body")
                if body:
                    for child in body.named_children:
                        if child.type == part_name:
                            candidates.append(child)
            else:
                # if part_name is not a field or statement type, just skip it
                continue

        for cand in candidates:
            expr = clean_string(cand.text.decode("utf-8"))
            sr, sc = cand.start_point
            er, ec = cand.end_point
            part_id = str(uuid.uuid4())

            defs_part = []
            uses_part = []
            # Use the same scope as the parent statement for all parts
            # This ensures condition and consequence use the same scope for variable resolution
            parent_scope = scope_manager.get_scope_for_node(node)
            walk_defs_uses(cand, field_role_map, defs_part, uses_part,
                           role="use", scope_manager=scope_manager, stmt_scope=parent_scope,
                           call_role_map=call_role_map, id_type_str="variable")
            
            parts.append({
                "id": part_id,
                "part_nname": part_name,
                "expression": expr,
                "start": [sr, sc],
                "end": [er, ec],
                "left_side": defs_part,
                "right_side": uses_part
            })
    return parts

#
# ────────────────────────────────────────────────────────────────────────────────
#  7. attach_sub_statements_by_range
# ────────────────────────────────────────────────────────────────────────────────
#
def attach_sub_statements_by_range(statements):
    """
    Mutates `statements` in-place:
        for each stmt S that has S['parts'] = [part1, ...]:
            - parse each parts start/end
            - scan all stmts T in `statements`
            - If T.start >= part.start and T.end <= part.end, add T.id to part['statement_ids]
            and tags T['additional_info'] with {'part_of': part_id}
    """
    def le_pos(a, b):
        """
        Compare two positions (tuples of (line, col)) for less than or equal.
        """
        return (a[0] < b[0]) or (a[0] == b[0] and a[1] <= b[1])

    def parse_pos(p):
        # p can be [line, col] or "line:col"
        if isinstance(p, (list, tuple)):
            return (int(p[0]), int(p[1]))
        if isinstance(p, str):
            l, c = p.split(":", 1)
            return (int(l), int(c))
        raise ValueError(f"Invalid position format: {p}")
    
    # build list of (stmt_id, start, end, stmt_obj) for all stmts
    indexed = []
    for stmt in statements:
        s_start = parse_pos(stmt['start'])
        s_end = parse_pos(stmt['end'])
        indexed.append((stmt['id'], s_start, s_end, stmt))

    for stmt in statements:
        for part in stmt.get('parts', []):
            p_start = parse_pos(part['start'])
            p_end = parse_pos(part['end'])
            part_ids = []

            for sid, s_start, s_end, other in indexed:
                if sid == stmt['id']:
                    continue
                if le_pos(p_start, s_start) and le_pos(s_end, p_end):
                    part_ids.append(sid)
                    other.setdefault('additional_info', []).append({'part_of': part['id']})

            part['statement_ids'] = part_ids

#
# ────────────────────────────────────────────────────────────────────────────────
#  8. analyze_function_ast
# ────────────────────────────────────────────────────────────────────────────────
#
def analyze_function_ast(function_node):
    """
    Analyzes the AST of a function node to determine the data flow and dependencies between the nodes.
    :param function_node: The function node to analyze
    :return: A dictionary containing the data flow and dependencies between the nodes
    """
    results = {
        "parameters": [],
        "statements": []
    }

    scope_manager = ScopeManager()
    func_scope = scope_manager.enter_scope(function_node.id)

    statement_types = ctf_mapping.get("statement_types", [])
    # control_flow_types = ctf_mapping.get("control_flow_types", [])

    # Build function name - handle various function definition styles including macros
    fn_type_node = function_node.child_by_field_name('type')
    fn_decl_node = function_node.child_by_field_name('declarator')

    fn_type_text = ""
    fn_decl_text = ""

    if fn_type_node:
        fn_type_text = fn_type_node.text.decode('utf-8')

    if fn_decl_node:
        fn_decl_text = fn_decl_node.text.decode('utf-8')
    else:
        # For macro-style functions like PHP_MINFO_FUNCTION(mcrypt), the structure is different
        # Try to extract name from direct children
        for child in function_node.children:
            if child.type == "type_identifier":
                fn_type_text = child.text.decode('utf-8')
            elif child.type == "parenthesized_declarator":
                fn_decl_text = child.text.decode('utf-8')
            elif child.type == "identifier" and not fn_decl_text:
                fn_decl_text = child.text.decode('utf-8')

    # Combine type and declarator to form the function name
    fn_name = f"{fn_type_text} {fn_decl_text}".strip()
    if not fn_name:
        # Last resort: use the first line of the function text
        fn_name = function_node.text.decode('utf-8').split('\n')[0].split('{')[0].strip()

    fn_def_stmt = {
        "id": str(uuid.uuid4()),
        "type": "function_definition",
        "name":  fn_name,
        "expression": fn_name + " {",
        "start": function_node.start_point,
        "end": function_node.end_point,
        "scope_level": scope_manager.current_scope.depth,
        "left_side": [],
        "right_side": [],
        "parameters": [],
        "parts": [],
        "additional_info": []
    }
    results["statements"].append(fn_def_stmt)

    # Register function parameters
    # For standard functions: function_node->declarator->parameters
    # For macro functions: the structure may differ
    fn_decl = function_node.child_by_field_name("declarator")
    fn_param_decl = None

    # `char *f(...)` / `int (*f(...))[3]`: the declarator is a pointer_declarator
    # (or parenthesized_declarator) wrapping the function_declarator
    while fn_decl is not None and fn_decl.type != "function_declarator":
        inner = fn_decl.child_by_field_name("declarator")
        if inner is None:
            break
        fn_decl = inner

    if fn_decl:
        fn_param_decl = fn_decl.child_by_field_name("parameters")
    else:
        # Try to find parameters in alternative structures (macro-style functions)
        # Look for a parenthesized_declarator or direct parameter_list
        for child in function_node.children:
            if child.type == "parameter_list":
                fn_param_decl = child
                break
            elif child.type == "function_declarator":
                fn_param_decl = child.child_by_field_name("parameters")
                if fn_param_decl:
                    break

    if fn_param_decl:
        for idx, (pname, pid_node) in enumerate(extract_parameter_identifiers(fn_param_decl)):
            scope_manager.declare(pname, pid_node.id)
            r, c = pid_node.start_point
            param_entry = {
                "name": pname,
                "position": [r, c],
                "arg_pos": idx
            }
            results["parameters"].append(param_entry)
            fn_def_stmt["parameters"].append({
                "name": pname,
                "var_id": scope_manager.resolve(pname, scope_manager.current_scope).id,
                "position_start": [r, c],
                "position_end": list(pid_node.end_point)
            })

    # Register declarations in the function body
    body = function_node.child_by_field_name("body")
    if body:
        # Don't create a new scope for the function body since we already have the function scope
        # Just register declarations within the current function scope
        for child in body.named_children:
            register_declarations(child, scope_manager)
    else:
        return results
    
    # Collect all "statements" in the function body
    stmt_nodes = []
    collect_statements(body, statement_types, stmt_nodes)

    # PRINT DEBUG INFO
    # print(f"Found {len(stmt_nodes)} statements in function {fn_name}.")
    # for stmt in stmt_nodes:
    #     print(f"Statement: {stmt.text.decode('utf-8')} (type={stmt.type}, id={stmt.id})")


    # scope_manager.print_state()

    # For each statement node, comnpute def/use + calls
    for node in stmt_nodes:
        sr, sc = node.start_point
        er, ec = node.end_point

        # Get node text with comments stripped to ensure comment-only changes
        # don't get detected as actual code changes
        expr_text = clean_string(get_node_text_without_comments(node))

        # Find nearest compund_statement scope for this node
        stmt_scope = scope_manager.get_scope_for_node(node, fallback=func_scope)
        sid = stmt_scope.scope_id if stmt_scope else None
        depth = stmt_scope.depth if stmt_scope else 0

        # compute "scope level" by counting compound_statement ancestors
        lvl = 0
        tmp = node.parent
        while tmp is not None:
            if tmp.type == "compound_statement":
                lvl += 1
            tmp = tmp.parent

        # walk defs & uses, and take call role for call_expressions into account
        defs_list = []
        uses_list = []
        walk_defs_uses(node, field_role_map, defs_list, uses_list,
                       role="use", scope_manager=scope_manager, stmt_scope=stmt_scope,
                       call_role_map=ctf_mapping.get("call_role_map", []), id_type_str="variable")
        
        left_side = defs_list[:]
        right_side = uses_list[:]

        # Record call_expression details (arg_pos, etc.) for this statement
        calls_info = []
        to_visit = [node]
        while to_visit:
            cur = to_visit.pop()
            if cur.type == "call_expression":
                fn_node = cur.child_by_field_name("function")
                func_name = ""
                if fn_node and fn_node.type == "identifier":
                    func_name = fn_node.text.decode("utf-8")
                elif fn_node:
                    # case of more complex callee (e.g. *(fptr)(arg1, arg2)), just extract text
                    func_name = clean_string(fn_node.text.decode("utf-8"))

                cr, cc = cur.start_point
                cer, cec = cur.end_point
                args_node = cur.child_by_field_name("arguments")
                args_list = []
                if args_node:
                    for idx, arg in enumerate(a for a in args_node.named_children
                                              if is_valid_argument_node(a)):
                        arg_text = clean_string(arg.text.decode("utf-8"))
                        ar, ac = arg.start_point
                        aer, aec = arg.end_point
                        args_list.append({
                            "name": arg_text,
                            "position_start": [ar, ac],
                            "position_end": [aer, aec],
                            "arg_pos": idx
                        })
                calls_info.append({
                    "function_name": func_name,
                    "position_start": [cr, cc],
                    "position_end": [cer, cec],
                    "arguments": args_list
                })
            
            to_visit.extend(cur.named_children)

        # Create the statement entry
        stmt_entry = {
            "id": str(uuid.uuid4()),
            "type": node.type,
            "expression": expr_text,
            "start": [sr, sc],
            "end": [er, ec],
            "scope_id": sid,
            "scope_depth": depth,
            "scope_level": lvl,
            "left_side": left_side,
            "right_side": right_side,
            "calls_info": calls_info,
            "parts": [],
            "additional_info": []
        }

        stmt_entry["parts"] = generate_statement_parts(
            node, field_role_map, ctf_mapping.get("statement_parts", {}),
            scope_manager, ctf_mapping.get("call_role_map", []), statement_types
        )

        # Add the statement entry to results
        results["statements"].append(stmt_entry)

    # Attach sub-statements to parts by range
    attach_sub_statements_by_range(results["statements"])

    return results

def analyze_function_ast_global(root_node):
    """
    Analyzes the AST of a function node to determine the data flow and dependencies between the nodes.
    :param function_node: The function node to analyze
    :return: A dictionary containing the data flow and dependencies between the nodes
    """
    results = {
        "statements": []
    }

    scope_manager = ScopeManager()
    func_scope = scope_manager.enter_scope(root_node.id)

    statement_types = [
        "declaration",
        "type_definition", 
        "preproc_if",
        "preproc_ifdef",
        "preproc_else", 
        "preproc_elif",
        "preproc_elifdef",
        "preproc_include",
        "preproc_def",
        "preproc_function_def",
        "preproc_call",
        "linkage_specification",
        "_empty_declaration",
        "struct_specifier",
        "union_specifier",
        "enum_specifier",
        "macro_type_specifier",
        "sized_type_specifier",
        "_type_identifier",
        "field_declaration",
        "enumerator"
    ]
    # control_flow_types = ctf_mapping.get("control_flow_types", [])

    register_declarations(root_node, scope_manager)
    
    # For global context analysis, only collect statements from non-function nodes
    # Function definitions will be analyzed separately
    relevant_nodes = []
    for child in root_node.named_children:
        if child.type != "function_definition":
            relevant_nodes.append(child)
    
    # Collect all "statements" from relevant (non-function) nodes
    stmt_nodes = []
    for node in relevant_nodes:
        collect_statements(node, statement_types, stmt_nodes)


    # For each statement node, comnpute def/use + calls
    for node in stmt_nodes:
        sr, sc = node.start_point
        er, ec = node.end_point

        # Get node text with comments stripped to ensure comment-only changes
        # don't get detected as actual code changes
        expr_text = clean_string(get_node_text_without_comments(node))

        # Find nearest compund_statement scope for this node
        stmt_scope = scope_manager.get_scope_for_node(node, fallback=func_scope)
        sid = stmt_scope.scope_id if stmt_scope else None
        depth = stmt_scope.depth if stmt_scope else 0

        # compute "scope level" by counting compound_statement ancestors
        lvl = 0
        tmp = node.parent
        while tmp is not None:
            if tmp.type == "compound_statement":
                lvl += 1
            tmp = tmp.parent

        # walk defs & uses, and take call role for call_expressions into account
        defs_list = []
        uses_list = []
        walk_defs_uses(node, field_role_map, defs_list, uses_list,
                       role="use", scope_manager=scope_manager, stmt_scope=stmt_scope,
                       call_role_map=[], id_type_str="variable")
        
        left_side = defs_list[:]
        right_side = uses_list[:]

        # Record call_expression details (arg_pos, etc.) for this statement
        calls_info = []
        to_visit = [node]
        while to_visit:
            cur = to_visit.pop()
            if cur.type == "call_expression":
                fn_node = cur.child_by_field_name("function")
                func_name = ""
                if fn_node and fn_node.type == "identifier":
                    func_name = fn_node.text.decode("utf-8")
                elif fn_node:
                    # case of more complex callee (e.g. *(fptr)(arg1, arg2)), just extract text
                    func_name = clean_string(fn_node.text.decode("utf-8"))

                cr, cc = cur.start_point
                cer, cec = cur.end_point
                args_node = cur.child_by_field_name("arguments")
                args_list = []
                if args_node:
                    for idx, arg in enumerate(a for a in args_node.named_children
                                              if is_valid_argument_node(a)):
                        arg_text = clean_string(arg.text.decode("utf-8"))
                        ar, ac = arg.start_point
                        aer, aec = arg.end_point
                        args_list.append({
                            "name": arg_text,
                            "position_start": [ar, ac],
                            "position_end": [aer, aec],
                            "arg_pos": idx
                        })
                calls_info.append({
                    "function_name": func_name,
                    "position_start": [cr, cc],
                    "position_end": [cer, cec],
                    "arguments": args_list
                })
            
            to_visit.extend(cur.named_children)

        # Create the statement entry
        stmt_entry = {
            "id": str(uuid.uuid4()),
            "type": node.type,
            "expression": expr_text,
            "start": [sr, sc],
            "end": [er, ec],
            "scope_id": sid,
            "scope_depth": depth,
            "scope_level": lvl,
            "left_side": left_side,
            "right_side": right_side,
            "calls_info": calls_info,
            "parts": [],
            "additional_info": []
        }

        stmt_entry["parts"] = generate_statement_parts(
            node, field_role_map, ctf_mapping.get("statement_parts", {}),
            scope_manager, [], statement_types
        )

        # Add the statement entry to results
        results["statements"].append(stmt_entry)

    # Attach sub-statements to parts by range
    attach_sub_statements_by_range(results["statements"])

    return results
    



def create_ast_json(file_path, line_number):
    """
    Create an AST file froma  given source code file
    """

    parser = SourceCodeParserC(file_path)
    function_node = parser.find_function_containing_line(line_number)
    result = analyze_function_ast(function_node)
    json_result = convert_to_json_compatible(result)

    return json_result

def _without_comments(line):
    return re.sub(r"//.*", "", re.sub(r"/\*.*?\*/", " ", line))


def create_ast_json_region(file_path, start_line0):
    """`create_ast_json` for a definition tree-sitter does not parse as a
    function_definition: a macro-defined header (`PHP_METHOD(Phar, mount)
    { … }`), a function wrapped into an ERROR node by an embedded-GLSL macro,
    or one merged with its neighbour by a parse error. The text from the
    header at `start_line0` (0-based) to the next closing brace at column 0
    is parsed as a synthetic function, line numbers preserved (the header
    lines are blanked, the body is untouched). Returns None without a body."""
    parser = SourceCodeParserC(file_path)
    lines = parser.get_code().split("\n")
    open_line = None
    for j in range(start_line0, min(start_line0 + 12, len(lines))):
        text = _without_comments(lines[j])
        if "{" in text:
            open_line = j
            break
        if ";" in text:          # a prototype, not a definition
            return None
    if open_line is None:
        return None
    end = next((j for j in range(open_line + 1, len(lines)) if lines[j].startswith("}")), None)
    if end is None:
        return None
    body_start = _without_comments(lines[open_line])
    region = [""] * open_line
    region.append("int __crossslice_caller__(void) " + body_start[body_start.index("{"):])
    region += lines[open_line + 1:end + 1]
    synthetic = SourceCodeParserC.from_source("\n".join(region), file_path)
    function_node = synthetic.find_function_containing_line(open_line)
    if function_node is None:
        return None
    return convert_to_json_compatible(analyze_function_ast(function_node))


def create_ast_json_global(file_path):
    """
    Create an AST file froma  given source code file
    """

    parser = SourceCodeParserC(file_path)
    root_node = parser.get_top_level_node()
    result = analyze_function_ast_global(root_node)
    json_result = convert_to_json_compatible(result)

    return json_result


if __name__ == "__main__":
    line_number = 5  # Example line number
    

    
