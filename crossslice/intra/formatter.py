import json
import difflib
from typing import List, Dict, Any, Set, Optional
import os
import numpy as np

class Formatter:
    """
    Modular, language-agnostic code formatter for merged statement data.
    
    This formatter outputs only relevant control flow parts and changed/inserted/deleted statements,
    following these rules:
    1. Always output function definition at the top
    2. For control flow statements: always output condition/initializer/update parts, 
       only output changed/inserted/deleted body statements
    3. Use proper diff markers: [DEL], [ADD], [MOD]
    4. Maintain correct code order and structure
    """
    
    def __init__(self, control_flow_mapping_file: str = None, language: str = "c", merged_statements: List[Dict[str, Any]] = None):
        """
        Initialize the formatter with language-specific control flow mapping.
        
        Args:
            control_flow_mapping_file: Path to control flow mapping JSON file
            language: Programming language (default: "c")
        """
        self.language = language
        self.control_flow_mapping = self._load_control_flow_mapping(control_flow_mapping_file)

        self.block_increase_stmts = {
            "if_statement", "switch_statement", "for_statement", "while_statement",
            "do_statement", "function_defintion", "case_statement", "default_statement",
            "preproc_if", "preproc_ifdef", "preproc_else", "preproc_elif", "preproc_elifdef"
        }

        self.scope_dict = {0: set()}  # Track scope depth and statement IDs
        self.processed_ids = set()
        self.scope_depth = 0

        # stacks for processing
        self.stmt_stack = []
        self.text_stack = []

        self.merged_statements = merged_statements if merged_statements is not None else []
        
    def _load_control_flow_mapping(self, mapping_file: str = None) -> Dict[str, Any]:
        """Load control flow mapping from JSON file."""
        if mapping_file is None:
            # Default path based on language
            script_dir = os.path.dirname(os.path.abspath(__file__))
            mapping_file = os.path.join(script_dir, f"data/control_flow_mapping_{self.language}.json")
        
        try:
            # with open(mapping_file, 'r') as f:
            #     return json.load(f)
            return {
                "control_flow_types": [
                    "if_statement", "switch_statement", "for_statement", 
                    "while_statement", "do_statement",
                    "case_statement", "default_statement",
                    "preproc_if", "preproc_ifdef", "preproc_else", 
                    "preproc_elif", "preproc_elifdef"
                ]
            }
        except FileNotFoundError:
            # Fallback basic mapping if file not found
            return {
                "control_flow_types": [
                    "if_statement", "switch_statement", "for_statement", 
                    "while_statement", "do_statement", "return_statement",
                    "break_statement", "continue_statement", "goto_statement",
                    "labeled_statement", "case_statement", "default_statement",
                    "preproc_if", "preproc_ifdef", "preproc_else", 
                    "preproc_elif", "preproc_elifdef"
                ],
                "statement_parts": {
                    "if_statement": ["condition", "consequence", "alternative"],
                    "for_statement": ["initializer", "condition", "update", "body"],
                    "while_statement": ["condition", "body"],
                    "switch_statement": ["condition", "case_statement"],
                    "preproc_if": ["condition", "consequence", "alternative"],
                    "preproc_ifdef": ["name", "consequence", "alternative"],
                    "preproc_else": ["consequence"],
                    "preproc_elif": ["condition", "consequence", "alternative"],
                    "preproc_elifdef": ["name", "consequence", "alternative"]
                }
            }
        
    def _combine_braces_and_remove_empty(self, text):
        lines = text.strip().splitlines()
        result = []
        buffer = ""

        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                continue
            
            # Collect standalone braces
            if stripped in ("{", "}"):
                buffer += stripped
            else:
                # If there are collected braces, add them as one line before the current line
                if buffer:
                    result.append(buffer)
                    buffer = ""
                result.append(line)
        
        # Add any remaining buffered braces
        if buffer:
            result.append(buffer)

        return "\n".join(result)
        
    def _get_indentation(self, depth: int) -> str:
        """Get indentation string based on depth."""
        # return "    " * depth
        return ""
    
    def _is_control_flow_statement(self, stmt_type: str) -> bool:
        """Check if a statement type is a control flow statement."""
        return stmt_type in self.control_flow_mapping.get("control_flow_types", [])
    
    def _is_inc_scope(self, stmt_type: str) -> bool:
        """Check if a statement type increases the scope (e.g., starts a block)."""
        return stmt_type in self.block_increase_stmts
    
    def _get_control_flow_parts(self, stmt_type: str) -> List[str]:
        """Get the list of parts for a control flow statement type."""
        return self.control_flow_mapping.get("statement_parts", {}).get(stmt_type, [])
    
    def _is_header_part(self, part_name: str) -> bool:
        """
        Determine if a part is a header part that should always be shown.
        Header parts include conditions, initializers, updates, etc.
        """
        header_parts = ["condition", "initializer", "update", "value", "test"]
        return part_name in header_parts
    
    def _character_diff(self, old: str, new: str) -> str:
        """
        Create character-level diff with [- ... -] {+ ... +} sections.
        Returns empty string if both old and new are empty.
        """
        if not old and not new:
            return ""
        
        if not old:
            return f"{{+ {new} +}}" if new.strip() else ""
        
        if not new:
            return f"[- {old} -]" if old.strip() else ""
        
        # Use SequenceMatcher for character-level diff
        matcher = difflib.SequenceMatcher(None, old, new)
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                result.append(old[i1:i2])
            elif tag == 'delete':
                deleted_text = old[i1:i2]
                if deleted_text.strip():
                    result.append(f"[- {deleted_text} -]")
            elif tag == 'insert':
                inserted_text = new[j1:j2]
                if inserted_text.strip():
                    result.append(f"{{+ {inserted_text} +}}")
            elif tag == 'replace':
                deleted_text = old[i1:i2]
                inserted_text = new[j1:j2]
                if deleted_text.strip():
                    result.append(f"[- {deleted_text} -]")
                if inserted_text.strip():
                    result.append(f"{{+ {inserted_text} +}}")
        
        return ''.join(result)
    
    def _word_diff(self, old: str, new: str) -> str:
        """
        Create word-level diff with [- ... -] {+ ... +} sections.
        Returns empty string if both old and new are empty.
        """
        if not old and not new:
            return ""
        
        if not old:
            return f"{{+ {new} +}}" if new.strip() else ""
        
        if not new:
            return f"[- {old} -]" if old.strip() else ""
        
        # Use SequenceMatcher for word-level diff
        matcher = difflib.SequenceMatcher(None, old.split(), new.split())
        result = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                result.append(' '.join(old.split()[i1:i2]))
            elif tag == 'delete':
                deleted_text = ' '.join(old.split()[i1:i2])
                if deleted_text.strip():
                    result.append(f"[- {deleted_text} -]")
            elif tag == 'insert':
                inserted_text = ' '.join(new.split()[j1:j2])
                if inserted_text.strip():
                    result.append(f"{{+ {inserted_text} +}}")
            elif tag == 'replace':
                deleted_text = ' '.join(old.split()[i1:i2])
                inserted_text = ' '.join(new.split()[j1:j2])
                if deleted_text.strip():
                    result.append(f"[- {deleted_text} -]")
                if inserted_text.strip():
                    result.append(f"{{+ {inserted_text} +}}")
        
        return ' '.join(result)
    
    def _get_change_marker(self, change_status: any) -> str:
        """Get the appropriate diff marker for a change status."""
        # Handle boolean modified flags
        if isinstance(change_status, bool):
            return "[MOD]" if change_status else ""

        # Handle string change status values
        markers = {
            "inserted": "[ADD]",
            "deleted": "[DEL]",
            "changed": "[MOD]",
            "moved": "[ADD]",  # Moved statement at new position (like git +)
            "moved_from": "[DEL]",  # Ghost showing where moved statement came from (like git -)
            "modified": "[MOD]"
        }
        return markers.get(change_status, "")
    
    def _format_struct_specifier_expression(self, stmt: Dict[str, Any], scope_depth: int) -> str:
        """
        Format a struct specifier expression with appropriate diff markers.
        
        Args:
            stmt: Struct specifier statement dictionary
            scope_depth: Current scope depth
            
        Returns:
            Formatted string for the struct specifier
        """
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        indentation = self._get_indentation(scope_depth)

        # get the struct name till the opening brace
        old_struct_name = old_expression.split("{")[0].strip() if old_expression else ""
        new_struct_name = new_expression.split("{")[0].strip() if new_expression else ""
        if old_struct_name and new_struct_name and old_struct_name != new_struct_name:
            diff_result = self._diff_function(old_struct_name, new_struct_name)
            if diff_result.strip():
                expression = f"{diff_result} {{"
            else:
                expression = f"{new_struct_name} {{"
        else:
            expression = f"{expression.split('{')[0].strip()} {{"

        first_line = ""
        if change_status == "inserted":
            first_line = f"{indentation}[ADD] {expression}"
        elif change_status == "deleted":
            first_line = f"{indentation}[DEL] {expression}"
        elif change_status == "moved_from":
            # Ghost deleted entry showing where a moved struct came from
            first_line = f"{indentation}[DEL] {expression}"
        elif change_status == "changed":
            if old_expression and new_expression and old_expression != new_expression:
                # diff_result = self._diff_function(old_expression, new_expression)
                diff_result = expression
                if diff_result.strip():
                    first_line = f"{indentation}[MOD] {diff_result}"
                else:
                    first_line = f"{indentation}[MOD] {expression}"
            else:
                first_line = f"{indentation}[MOD] {expression}"
        elif change_status == "moved":
            # Moved struct at its new position
            first_line = f"{indentation}[ADD] {expression}"
        else:
            first_line = f"{indentation}{expression}"

        # handle the body of the struct
        fields_stmt_ids = set()
        if stmt.get("additional_info", []):
            for info in stmt["additional_info"]:
                if info.get("info") == "contained_statements":
                    fields_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("old_statement"):
            old_stmt = stmt.get("old_statement", {})
            if old_stmt.get("additional_info", []):
                for info in old_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        fields_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("new_statement"):
            new_stmt = stmt.get("new_statement", {})
            if new_stmt.get("additional_info", []):
                for info in new_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        fields_stmt_ids.update(info.get("stmt_ids", []))

        if fields_stmt_ids:
            body_lines = []
            for stmt in self.merged_statements:
                if stmt.get("id") in fields_stmt_ids:
                    formatted_stmt = self._format_normal_stmt(stmt, scope_depth + 1)
                    if formatted_stmt:
                        body_lines.append(formatted_stmt)
                    # Mark statement as processed to avoid duplicate processing
                    self.processed_ids.add(stmt.get("id"))
            if body_lines:
                body_text = "\n".join(body_lines)
                return f"{first_line}\n{body_text}\n{indentation}}}"
            else:
                return f"{first_line}\n{indentation}}}"
        else:
            return f"{first_line}\n{indentation}}}"

    def _format_enum_specifier_expression(self, stmt: Dict[str, Any], scope_depth: int) -> str:
        """
        Format an enum specifier expression with appropriate diff markers.
        
        Args:
            stmt: Enum specifier statement dictionary
            scope_depth: Current scope depth
            
        Returns:
            Formatted string for the enum specifier
        """
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        indentation = self._get_indentation(scope_depth)

        # get the enum name till the opening brace
        old_enum_name = old_expression.split("{")[0].strip() if old_expression else ""
        new_enum_name = new_expression.split("{")[0].strip() if new_expression else ""
        if old_enum_name and new_enum_name and old_enum_name != new_enum_name:
            diff_result = self._diff_function(old_enum_name, new_enum_name)
            if diff_result.strip():
                expression = f"{diff_result} {{"
            else:
                expression = f"{new_enum_name} {{"
        else:
            expression = f"{expression.split('{')[0].strip()} {{"

        first_line = ""
        if change_status == "inserted":
            first_line = f"{indentation}[ADD] {expression}"
        elif change_status == "deleted":
            first_line = f"{indentation}[DEL] {expression}"
        elif change_status == "moved_from":
            # Ghost deleted entry showing where a moved enum came from
            first_line = f"{indentation}[DEL] {expression}"
        elif change_status == "changed":
            if old_expression and new_expression and old_expression != new_expression:
                diff_result = expression
                if diff_result.strip():
                    first_line = f"{indentation}[MOD] {diff_result}"
                else:
                    first_line = f"{indentation}[MOD] {expression}"
            else:
                first_line = f"{indentation}[MOD] {expression}"
        elif change_status == "moved":
            # Moved enum at its new position
            first_line = f"{indentation}[ADD] {expression}"
        else:
            first_line = f"{indentation}{expression}"

        # handle the body of the enum (enumerators)
        enum_stmt_ids = set()
        if stmt.get("additional_info", []):
            for info in stmt["additional_info"]:
                if info.get("info") == "contained_statements":
                    enum_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("old_statement"):
            old_stmt = stmt.get("old_statement", {})
            if old_stmt.get("additional_info", []):
                for info in old_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        enum_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("new_statement"):
            new_stmt = stmt.get("new_statement", {})
            if new_stmt.get("additional_info", []):
                for info in new_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        enum_stmt_ids.update(info.get("stmt_ids", []))

        if enum_stmt_ids:
            body_lines = []
            for stmt in self.merged_statements:
                if stmt.get("id") in enum_stmt_ids:
                    formatted_stmt = self._format_normal_stmt(stmt, scope_depth + 1)
                    if formatted_stmt:
                        body_lines.append(formatted_stmt)
                    # Mark statement as processed to avoid duplicate processing
                    self.processed_ids.add(stmt.get("id"))
            if body_lines:
                body_text = "\n".join(body_lines)
                return f"{first_line}\n{body_text}\n{indentation}}}"
            else:
                return f"{first_line}\n{indentation}}}"
        else:
            return f"{first_line}\n{indentation}}}"

    
    def _format_statement_expression(self, stmt: Dict[str, Any], scope_depth: int) -> str:
        """
        Format a statement expression with appropriate diff markers.
        """
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        indentation = self._get_indentation(scope_depth)
        
        if change_status == "inserted":
            return f"{indentation}[ADD] {expression}"
        elif change_status == "deleted":
            return f"{indentation}[DEL] {expression}"
        elif change_status == "moved_from":
            # Ghost deleted entry showing where a moved statement came from
            return f"{indentation}[DEL] {expression}"
        elif change_status == "changed" or change_status == "modified":
            if old_expression and new_expression and old_expression != new_expression:
                # Use character-level diff for fine-grained changes
                diff_result = self._diff_function(old_expression, new_expression)
                if diff_result.strip():
                    return f"{indentation}[MOD] {diff_result}"
                else:
                    return f"{indentation}[MOD] {expression}"
            elif change_status == "changed" and stmt.get("match_id") is None:
                # Statement got inserted, but not changed
                return f"{indentation}[ADD] {expression}"
            else:
                return f"{indentation}[MOD] {expression}"
        elif change_status == "moved":
            # Moved statement at its new position (shown with [ADD])
            # The ghost deleted entry shows where it was (with [DEL])
            return f"{indentation}[ADD] {expression}"
        else:
            # No change marker for unchanged statements
            return f"{indentation}{expression}"
    
    def _should_include_statement(self, stmt: Dict[str, Any], parent_changes: Set[str] = None) -> bool:
        """
        Determine if a statement should be included in the output.
        
        Args:
            stmt: Statement dictionary
            parent_changes: Set of statement IDs that have changes in the parent
        """
        stmt_id = stmt.get("id", "")
        change_status = stmt.get("change_status", "")
        
        # Always include changed, inserted, deleted, or moved statements
        if change_status in ["changed", "inserted", "deleted", "moved", "moved_from"]:
            return True
        
        # Include if this statement ID is mentioned in parent changes
        if parent_changes and stmt_id in parent_changes:
            return True
        
        # Include if this statement has inner changes
        inner_changes = stmt.get("additional_info", [])
        for info in inner_changes:
            if info.get("info") == "inner_changes" and info.get("changes"):
                return True
        
        return False

    def _should_include_in_body(self, stmt_obj: Dict[str, Any], body_stmt_ids: list) -> bool:
        """
        Determine if a statement should be included in a control flow body.

        This extends the normal relevance check to also include return statements
        when the body otherwise has no relevant statements. This is important for
        security analysis since early returns affect control flow paths.

        Args:
            stmt_obj: Statement dictionary to check
            body_stmt_ids: List of all statement IDs in this body

        Returns:
            True if statement should be included in output
        """
        # Standard inclusion: relevant to dataflow or has changes
        if stmt_obj.get("relevant_to_dataflow", False):
            return True
        if stmt_obj.get("change_status", "") not in ["matched", ""]:
            return True

        # Additional check: include return statements if body has no other relevant statements
        if stmt_obj.get("type") == "return_statement":
            # Check if any OTHER statement in this body is relevant
            has_other_relevant = False
            for other_id in body_stmt_ids:
                if other_id == stmt_obj.get("id"):
                    continue
                # Find the other statement
                for other_stmt in self.merged_statements:
                    if other_stmt.get("id") == other_id:
                        if other_stmt.get("relevant_to_dataflow", False):
                            has_other_relevant = True
                            break
                        if other_stmt.get("change_status", "") not in ["matched", ""]:
                            has_other_relevant = True
                            break
                if has_other_relevant:
                    break

            # If no other statement is relevant, include this return statement
            if not has_other_relevant:
                return True

        return False

    def _function_defitnion(self, func_stmt: Dict[str, Any]) -> str:
        """
        Format a function definition statement.

        Args:
            func_stmt: Function definition statement dictionary

        Returns:
            Formatted string for the function definition
        """
        func_expr = func_stmt.get("expression", "")
        func_expr_old = func_stmt.get("old_expression", "")
        change_status = func_stmt.get("change_status", "")

        if func_expr_old != "" and func_expr != func_expr_old:
            diff_result = self._character_diff(func_expr_old, func_expr)
            if diff_result.strip():
                return f"[MOD] {diff_result}"
            else:
                return f"[MOD] {func_expr}"
        elif change_status == "inserted":
            return f"[ADD] {func_expr}"
        elif change_status == "deleted":
            return f"[DEL] {func_expr}"
        elif change_status == "moved":
            return f"[ADD] {func_expr}"
        elif change_status == "moved_from":
            return f"[DEL] {func_expr}"
        else:
            return func_expr

    def _get_ctrl_flow_part_obj(self, stmt: Dict[str, Any], part_name: str, part_index_new: int = 0, part_index_old: int = 0) -> Optional[Dict[str, Any]]:
        parts = stmt.get("parts", [])
        stmt_id = stmt.get("id", "")
        if not parts or len(parts) < 1:
            return None

        is_changed = True if stmt.get("old_statement") is not None else False
        stmt_status = stmt.get("change_status", "")
        stmt_ids = set()
        modified = ""
        expression = ""

        parts_new = [p for p in parts if p.get("part_nname") == part_name]
        part_new = parts_new[part_index_new] if parts_new and part_index_new < len(parts_new) else None

        if is_changed:
            old_stmt = stmt.get("old_statement")
            old_parts = old_stmt.get("parts", [])
            parts_old = [p for p in old_parts if p.get("part_nname") == part_name]
            part_old = parts_old[part_index_old] if parts_old and part_index_old < len(parts_old) else None

            if part_new is None and part_old is None:
                return None

            if part_new and part_new.get("statement_ids"):
                stmt_ids.update(part_new.get("statement_ids", []))
            if part_old and part_old.get("statement_ids"):
                stmt_ids.update(part_old.get("statement_ids", []))

            if stmt_status in ("changed", "matched", "moved"):

                if part_new and part_old and part_new.get("expression") != part_old.get("expression"):
                    modified = "modified"
                    # expression = self._character_diff(part_old.get("expression", ""), part_new.get("expression", ""))
                    expression = self._diff_function(part_old.get("expression", ""), part_new.get("expression", ""))
                elif part_new is None and part_old is not None:
                    modified = "deleted"
                    # expression = self._character_diff(part_old.get("expression", ""), "")
                    expression = self._diff_function(part_old.get("expression", ""), "")
                elif part_new is not None and part_old is None:
                    modified = "inserted"
                    # expression = self._character_diff("", part_new.get("expression", ""))
                    expression = self._diff_function("", part_new.get("expression", ""))
                else:
                    expression = part_new.get("expression", "")

                    if stmt_status == "inserted":
                        modified = "inserted"
                    elif stmt_status == "deleted":
                        modified = "deleted"
                    elif stmt_status == "moved":
                        modified = "moved"
            elif stmt_status == "":
                if part_new and part_old:
                    if part_new.get("expression") != part_old.get("expression"):
                        modified = "modified"
                        # expression = self._character_diff(part_old.get("expression", ""), part_new.get("expression", ""))
                        expression = self._diff_function(part_old.get("expression", ""), part_new.get("expression", ""))
                    else:
                        expression = part_new.get("expression", "")
                elif part_new is None and part_old is not None:
                    # expression = self._character_diff(part_old.get("expression", ""), "")
                    expression = self._diff_function(part_old.get("expression", ""), "")
                elif part_new is not None and part_old is None:
                    # expression = self._character_diff("", part_new.get("expression", ""))
                    expression = self._diff_function("", part_new.get("expression", ""))

        else:
            if part_new is None:
                # pass
                # print(f"Warning: Part '{part_name}' not found in statement {stmt.get('id', 'unknown')}")
                # print(f"Statement: {stmt}")
                return None

            if part_new and part_new.get("statement_ids", []):
                stmt_ids.update(part_new.get("statement_ids", []))

            if stmt_status == "moved_from":
                # Ghost deleted entry - mark as moved_from
                modified = "moved_from"
                expression = part_new.get("expression", "")
            elif stmt_status == "deleted":
                # Deleted statement - mark as deleted
                modified = "deleted"
                expression = part_new.get("expression", "")
            elif stmt_status == "inserted" or (stmt_status != "matched" and stmt.get("match_id") is None):
                modified = "inserted"
                expression = part_new.get("expression", "")
            else:
                expression = part_new.get("expression", "")

        return {
            "part_name": part_name,
            "expression": expression,
            "modified": modified,
            "statement_ids": list(stmt_ids)
        }

    def _get_git_ctrl_flow_part_obj(self, stmt: Dict[str, Any], part_name: str, part_index_new: int = 0, part_index_old: int = 0) -> Optional[Dict[str, Any]]:
        """
        Get control flow part object for git diff format.
        Returns both old and new expressions separately instead of inline diff.
        """
        parts = stmt.get("parts", [])
        stmt_id = stmt.get("id", "")
        if not parts or len(parts) < 1:
            return None

        is_changed = True if stmt.get("old_statement") is not None else False
        stmt_status = stmt.get("change_status", "")
        stmt_ids = set()
        modified = ""
        old_expression = ""
        new_expression = ""

        parts_new = [p for p in parts if p.get("part_nname") == part_name]
        part_new = parts_new[part_index_new] if parts_new and part_index_new < len(parts_new) else None

        if is_changed:
            old_stmt = stmt.get("old_statement")
            old_parts = old_stmt.get("parts", [])
            parts_old = [p for p in old_parts if p.get("part_nname") == part_name]
            part_old = parts_old[part_index_old] if parts_old and part_index_old < len(parts_old) else None

            if part_new is None and part_old is None:
                return None

            if part_new and part_new.get("statement_ids"):
                stmt_ids.update(part_new.get("statement_ids", []))
            if part_old and part_old.get("statement_ids"):
                stmt_ids.update(part_old.get("statement_ids", []))

            if stmt_status in ("changed", "matched", "moved"):
                if part_new and part_old and part_new.get("expression") != part_old.get("expression"):
                    modified = "modified"
                    old_expression = part_old.get("expression", "")
                    new_expression = part_new.get("expression", "")
                elif part_new is None and part_old is not None:
                    modified = "deleted"
                    old_expression = part_old.get("expression", "")
                    new_expression = ""
                elif part_new is not None and part_old is None:
                    modified = "inserted"
                    old_expression = ""
                    new_expression = part_new.get("expression", "")
                else:
                    # Expressions are equal (or both exist)
                    old_expression = part_new.get("expression", "") or part_old.get("expression", "")
                    new_expression = part_new.get("expression", "") or part_old.get("expression", "")

                    if stmt_status == "inserted":
                        modified = "inserted"
                    elif stmt_status == "deleted":
                        modified = "deleted"
                    elif stmt_status == "moved":
                        modified = "moved"
            elif stmt_status == "":
                if part_new and part_old:
                    if part_new.get("expression") != part_old.get("expression"):
                        modified = "modified"
                        old_expression = part_old.get("expression", "")
                        new_expression = part_new.get("expression", "")
                    else:
                        old_expression = part_new.get("expression", "")
                        new_expression = part_new.get("expression", "")
                elif part_new is None and part_old is not None:
                    modified = "deleted"
                    old_expression = part_old.get("expression", "")
                    new_expression = ""
                elif part_new is not None and part_old is None:
                    modified = "inserted"
                    old_expression = ""
                    new_expression = part_new.get("expression", "")

        else:
            if part_new is None:
                return None

            if part_new and part_new.get("statement_ids", []):
                stmt_ids.update(part_new.get("statement_ids", []))

            if stmt_status == "moved_from":
                # Ghost deleted entry - use expression as old_expression
                modified = "moved_from"
                old_expression = part_new.get("expression", "")
                new_expression = ""
            elif stmt_status == "deleted":
                # Deleted statement - mark as deleted
                modified = "deleted"
                old_expression = part_new.get("expression", "")
                new_expression = ""
            elif stmt_status == "inserted" or (stmt_status != "matched" and stmt.get("match_id") is None):
                modified = "inserted"
                old_expression = ""
                new_expression = part_new.get("expression", "")
            else:
                old_expression = ""
                new_expression = part_new.get("expression", "")

        return {
            "part_name": part_name,
            "old_expression": old_expression,
            "new_expression": new_expression,
            "modified": modified,
            "statement_ids": list(stmt_ids)
        }
    
    def _format_normal_stmt(self, stmt: Dict[str, Any], scope_depth: int = 0, force_include: bool = False) -> str:
        stmt_id = stmt.get("id", "")
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        stmt_type = stmt.get("type", "")

        if stmt_id in self.processed_ids:
            return None  # Skip already processed statements

        # Same filtering logic as original, unless force_include is True
        if not force_include and stmt.get("relevant_to_dataflow", False) == False and change_status == "matched":
            # Skip matched statements or those not relevant to data flow
            return None
        
        # Handle struct and enum specifiers specially
        if stmt_type == "struct_specifier":
            formatted_lines = self._format_struct_specifier_expression(stmt, scope_depth)
            if formatted_lines:
                self.processed_ids.add(stmt_id)
                return formatted_lines
            return None
        elif stmt_type == "enum_specifier":
            formatted_lines = self._format_enum_specifier_expression(stmt, scope_depth)
            if formatted_lines:
                self.processed_ids.add(stmt_id)
                return formatted_lines
            return None
        
        is_ctrl_flow = self._is_control_flow_statement(stmt_type)
        if not is_ctrl_flow:
            # Format regular statements
            formatted_lines = self._format_statement_expression(stmt, scope_depth)
            if formatted_lines:
                self.processed_ids.add(stmt_id)
                return formatted_lines
            return None
        else:
            # Handle control flow statements separately
            self.processed_ids.add(stmt_id)
            return self._format_ctrl_flow_stmt(stmt)
        
            # return None

    def _format_ctrl_flow_stmt(self, stmt: Dict[str, Any]) -> str:
        """
        Format a control flow statement with proper indentation and diff markers.
        
        Args:
            stmt: Control flow statement dictionary
            
        Returns:
            Formatted string for the control flow statement
        """
        stmt_type = stmt.get("type", "")
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")

        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        line_txt = ""

        if self._is_inc_scope(stmt.get("type", "")) or stmt.get("expression", "").endswith("{"):
            self.scope_depth += 1

        if stmt_type == "function_definition":
            line_txt = self._function_defitnion(stmt)
            self.processed_ids.add(stmt.get("id", ""))
            return line_txt
        elif stmt_type == "if_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)

            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not condition_part:
                return self._format_statement_expression(stmt, self.scope_depth)
            if not consequence_part and not alternative_part:
                return self._format_statement_expression(stmt, self.scope_depth)

            # Format condition part
            condition_marker = self._get_change_marker(condition_part.get("modified", False))

            text_safe = {
                "condition": f"{self._get_indentation(self.scope_depth - 1)}{condition_marker + ' '}if {condition_part.get('expression', '')} {{\n",
                "consequence": "",
                "alternative": ""
            }
            line_txt = ""

            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                is_ghost_stmt = change_status == "moved_from"
                is_moved_stmt = change_status == "moved"
                for stmt_obj in self.merged_statements:
                    # Skip ghost statements that are only in the consequence because they're
                    # placeholders for moved statements - they'll be shown at their own position
                    if stmt_obj.get("change_status") == "moved_from" and stmt_obj.get("id", "").startswith("ghost_"):
                        continue
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Use _should_include_in_body to check if statement should be included
                        should_include = self._should_include_in_body(stmt_obj, consequence_stmt_ids)
                        if is_ghost_stmt:
                            # For ghost control flow statements, format the body statements with [DEL] markers
                            expr = stmt_obj.get("expression", "")
                            indentation = self._get_indentation(self.scope_depth)
                            formatted_stmt = f"{indentation}[DEL] {expr}"
                        elif is_moved_stmt:
                            # For moved control flow statements, format the body statements with [ADD] markers
                            expr = stmt_obj.get("expression", "")
                            indentation = self._get_indentation(self.scope_depth)
                            formatted_stmt = f"{indentation}[ADD] {expr}"
                        else:
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth, force_include=should_include)
                        if formatted_stmt:
                            text_safe["consequence"] += f"{formatted_stmt}\n"
                        # Don't add to processed_ids for ghost statements - the actual statement will be processed separately
                        if not is_ghost_stmt:
                            self.processed_ids.add(stmt_obj.get("id"))
                if text_safe["consequence"].strip() != "":
                    text_safe["consequence"] += f"{self._get_indentation(self.scope_depth - 1)}}}\n"
                self.scope_depth -= 1  # Decrease scope depth after block

            if alternative_part:
                alt_modified = alternative_part.get("modified", "")

                # For deleted alternative parts, don't try to show inner statements individually
                # - they may have moved to a new position (will be shown there)
                # - or they were truly deleted (would have change_status=deleted)
                # Just show the entire deleted else clause as a single deletion
                if alt_modified == "deleted":
                    alt_expr = alternative_part.get("expression", "")
                    if alt_expr:
                        text_safe["alternative"] = f"{self._get_indentation(self.scope_depth - 1)}[DEL] {alt_expr}\n"
                        # Mark only ghost statements referenced by the deleted alternative as processed
                        # so they don't get shown separately. Moved statements (change_status="moved")
                        # should NOT be marked as processed - they need to be shown at their new position.
                        alternative_stmt_ids = alternative_part.get("statement_ids", [])
                        for stmt_obj in self.merged_statements:
                            # Only mark ghost statements as processed, not moved statements
                            if stmt_obj.get("change_status") != "moved_from":
                                continue
                            matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                            if matches:
                                self.processed_ids.add(stmt_obj.get("id"))
                    else:
                        text_safe["alternative"] = ""
                else:
                    text_safe["alternative"] = f"{self._get_indentation(self.scope_depth - 1)}else {{\n"
                    temp_alt = ""
                    alternative_stmt_ids = alternative_part.get("statement_ids", [])
                    # For ghost/moved control flow statements, treat inner statements accordingly
                    is_ghost_stmt = change_status == "moved_from"
                    is_moved_stmt = change_status == "moved"
                    for stmt_obj in self.merged_statements:
                        # Use _stmt_matches_target_id to find matching statements
                        matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                        if matches:
                            # Use _should_include_in_body to check if statement should be included
                            should_include = self._should_include_in_body(stmt_obj, alternative_stmt_ids)
                            if is_ghost_stmt:
                                # For ghost control flow statements, format the body statements with [DEL] markers
                                expr = stmt_obj.get("expression", "")
                                indentation = self._get_indentation(self.scope_depth)
                                formatted_stmt = f"{indentation}[DEL] {expr}"
                            elif is_moved_stmt:
                                # For moved control flow statements, format the body statements with [ADD] markers
                                expr = stmt_obj.get("expression", "")
                                indentation = self._get_indentation(self.scope_depth)
                                formatted_stmt = f"{indentation}[ADD] {expr}"
                            else:
                                formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth, force_include=should_include)
                            if formatted_stmt:
                                temp_alt += f"{formatted_stmt}\n"
                            # Don't add to processed_ids for ghost statements
                            if not is_ghost_stmt:
                                self.processed_ids.add(stmt_obj.get("id"))
                    if temp_alt.strip() != "":
                        text_safe["alternative"] += temp_alt
                        text_safe["alternative"] += f"{self._get_indentation(self.scope_depth - 1)}}}\n"
                    else:
                        text_safe["alternative"] = ""
                self.scope_depth -= 1  # Decrease scope depth after block

            line_txt += text_safe["condition"]
            if text_safe["consequence"] != "":
                line_txt += text_safe["consequence"]
            elif text_safe["consequence"] == "":
                line_txt += "}"

            if text_safe["alternative"] != "":
                line_txt += text_safe["alternative"]

            return line_txt

        elif stmt_type == "switch_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            case_stmt_ids = set()
            
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")

            if not condition_part:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            case_parts_new = [p for p in parts if p.get("part_nname") == "case_statement"]
            for case_part in case_parts_new:
                if case_part.get("statement_ids"):
                    case_stmt_ids.update(case_part.get("statement_ids", []))

            old_stmt = stmt.get("old_statement")
            if old_stmt:
                case_parts_old = [p for p in old_stmt.get("parts", []) if p.get("part_nname") == "case_statement"]
                for case_part in case_parts_old:
                    if case_part.get("statement_ids"):
                        case_stmt_ids.update(case_part.get("statement_ids", []))
            
            # Format condition part
            condition_marker = self._get_change_marker(condition_part.get("modified", False))
            line_txt = f"{self._get_indentation(self.scope_depth - 1)}{condition_marker + ' ' if condition_marker else ''}switch ({condition_part.get('expression', '')}) {{\n"

            for stmt_obj in self.merged_statements:
                # Use _stmt_matches_target_id to find matching statements
                matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in case_stmt_ids)
                if matches:
                    formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                    if formatted_stmt:
                        line_txt += f"{formatted_stmt}\n"
                    # Mark statement as processed to avoid duplicate processing
                    self.processed_ids.add(stmt_obj.get("id"))

            line_txt += f"{self._get_indentation(self.scope_depth - 1)}}}\n"
            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "for_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)

            initializer_part = self._get_ctrl_flow_part_obj(stmt, "initializer")
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            update_part = self._get_ctrl_flow_part_obj(stmt, "update")
            body_part = self._get_ctrl_flow_part_obj(stmt, "body")

            # Check if the statement type itself changed (e.g., while -> for)
            old_stmt = stmt.get("old_statement", {})
            old_stmt_type = old_stmt.get("type", "")
            type_changed = old_stmt_type and old_stmt_type != stmt_type

            # Build for header
            init_expr = initializer_part.get("expression", "") if initializer_part else ""
            cond_expr = condition_part.get("expression", "") if condition_part else ""
            update_expr = update_part.get("expression", "") if update_part else ""

            header_txt = ""
            if type_changed:
                # Type changed (e.g., while(1) -> for(;;))
                # Show the old statement with [DEL] and new with [ADD]
                old_expr = stmt.get('old_expression', '') or old_stmt.get('expression', '')
                old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}[DEL] {old_header} {{\n"
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}[ADD] for ({init_expr}; {cond_expr}; {update_expr}) {{\n"
            else:
                # Check for modifications and get markers
                init_marker = self._get_change_marker(initializer_part.get("modified", False)) if initializer_part else ""
                cond_marker = self._get_change_marker(condition_part.get("modified", False)) if condition_part else ""
                update_marker = self._get_change_marker(update_part.get("modified", False)) if update_part else ""

                # Get the highest change marker
                # If any marker is [ADD] use [ADD], if any is [DEL] use [DEL], else use [MOD] if any part is modified
                if init_marker == "[ADD]" or cond_marker == "[ADD]" or update_marker == "[ADD]":
                    header_marker = "[ADD] "
                elif init_marker == "[DEL]" or cond_marker == "[DEL]" or update_marker == "[DEL]":
                    header_marker = "[DEL] "
                else:
                    # If any part is modified, mark the whole for statement
                    header_marker = "[MOD] " if init_marker or cond_marker or update_marker else ""

                header_txt = f"{self._get_indentation(self.scope_depth - 1)}{header_marker}for ({init_expr}; {cond_expr}; {update_expr}) {{\n"

            line_txt = ""

            # Format body statements
            if body_part:
                body_stmt_ids = body_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in body_stmt_ids)
                    if matches:
                        formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        # Mark statement as processed to avoid duplicate processing
                        self.processed_ids.add(stmt_obj.get("id"))

            if line_txt.strip() == "":
                # If no body statements, just close the for block
                line_txt = f"{header_txt}{self._get_indentation(self.scope_depth - 1)}}}\n"
            else:
                line_txt = header_txt + line_txt
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}}}\n"

            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "while_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)

            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            body_part = self._get_ctrl_flow_part_obj(stmt, "body")

            if not condition_part:
                return self._format_statement_expression(stmt, self.scope_depth)

            # Check if the statement type itself changed (e.g., for -> while)
            old_stmt = stmt.get("old_statement", {})
            old_stmt_type = old_stmt.get("type", "")
            type_changed = old_stmt_type and old_stmt_type != stmt_type

            header_txt = ""
            if type_changed:
                # Type changed (e.g., for(;;) -> while(1))
                # Show the old statement with [DEL] and new with [ADD]
                old_expr = stmt.get('old_expression', '') or old_stmt.get('expression', '')
                old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}[DEL] {old_header} {{\n"
                new_expr = condition_part.get('new_expression', '') or condition_part.get('expression', '')
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}[ADD] while ({new_expr}) {{\n"
            else:
                # Format condition part
                condition_marker = self._get_change_marker(condition_part.get("modified", False))
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}{condition_marker + ' ' if condition_marker else ''}while ({condition_part.get('expression', '')}) {{\n"

            line_txt = ""

            # Format body statements
            if body_part:
                body_stmt_ids = body_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in body_stmt_ids)
                    if matches:
                        formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        # Mark statement as processed to avoid duplicate processing
                        self.processed_ids.add(stmt_obj.get("id"))

            if line_txt.strip() == "":
                # If no body statements, just close the while block
                line_txt = f"{header_txt}{self._get_indentation(self.scope_depth - 1)}}}\n"
            else:
                line_txt = header_txt + line_txt
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}}}\n"

            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "do_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)

            body_part = self._get_ctrl_flow_part_obj(stmt, "body")
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")

            if not condition_part:
                return self._format_statement_expression(stmt, self.scope_depth)

            # Check if the statement type itself changed (e.g., for/while -> do-while)
            old_stmt = stmt.get("old_statement", {})
            old_stmt_type = old_stmt.get("type", "")
            type_changed = old_stmt_type and old_stmt_type != stmt_type

            header_txt = ""
            footer_txt = ""
            if type_changed:
                # Type changed - show old statement with [DEL]
                old_expr = stmt.get('old_expression', '') or old_stmt.get('expression', '')
                old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}[DEL] {old_header} {{\n"
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}[ADD] do {{\n"
                cond_expr = condition_part.get('new_expression', '') or condition_part.get('expression', '')
                footer_txt = f"{self._get_indentation(self.scope_depth - 1)}}} while ({cond_expr});\n"
            else:
                # Format do-while: body first, then condition
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}do {{\n"
                condition_marker = self._get_change_marker(condition_part.get("modified", False))
                footer_txt = f"{self._get_indentation(self.scope_depth - 1)}{condition_marker + ' ' if condition_marker else ''}}} while ({condition_part.get('expression', '')});\n"

            line_txt = ""

            # Format body statements
            if body_part:
                body_stmt_ids = body_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in body_stmt_ids)
                    if matches:
                        formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        # Mark statement as processed to avoid duplicate processing
                        self.processed_ids.add(stmt_obj.get("id"))

            if line_txt.strip() == "":
                # If no body statements, just close the do block
                line_txt = f"{header_txt}{self._get_indentation(self.scope_depth - 1)}}}\n"
            else:
                line_txt = header_txt + line_txt

            line_txt += footer_txt
            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "case_statement":
            # Case statements are handled within switch statements
            # If we encounter one standalone, treat it as a regular statement
            change_status = stmt.get("change_status", "")
            marker = self._get_change_marker(change_status)
            case_expr = stmt.get("expression", "")

            add_info = stmt.get("additional_info", [])
            contained_stmt_ids = set()
            for info in add_info:
                if info.get("info") == "contained_statements":
                    contained_stmt_ids.update(info.get("stmt_ids", []))

            parts = stmt.get("parts", [])
            header_txt = ""
            if not parts:
                # default case statement
                # return self._format_statement_expression(stmt, self.scope_depth)
                value_marker = self._get_change_marker(change_status)
                header_txt = f"{self._get_indentation(self.scope_depth)}{value_marker + ' ' if value_marker else ''}default:"
            else:
                value_part = self._get_ctrl_flow_part_obj(stmt, "value")
                if not value_part:
                    return self._format_statement_expression(stmt, self.scope_depth)
                
                value_marker = self._get_change_marker(value_part.get("modified", False))
                header_txt = f"{self._get_indentation(self.scope_depth)}{value_marker + ' ' if value_marker else ''}case {value_part.get('expression', '')}:"
            line_txt = ""

            if contained_stmt_ids:
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in contained_stmt_ids)
                    if matches:
                        formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        # Mark statement as processed to avoid duplicate processing
                        self.processed_ids.add(stmt_obj.get("id"))
            if line_txt.strip() == "":
                # If no contained statements, just return the header
                line_txt = f"{header_txt}\n"
            else:
                line_txt = f"{header_txt}\n" + line_txt
            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "default_statement":
            # Default statements are handled within switch statements
            # If we encounter one standalone, treat it as a regular statement
            change_status = stmt.get("change_status", "")
            marker = self._get_change_marker(change_status)
            line_txt = f"{self._get_indentation(self.scope_depth)}{marker + ' ' if marker else ''}default:"
            
            return line_txt

        # Handle preprocessor directives
        elif stmt_type == "preproc_if":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not condition_part:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""
            
            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) and stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_consequence_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) and stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_alternative_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            condition_changed = condition_part.get("modified", False) if condition_part else False

            # Determine if we need to show the #if header
            needs_header = has_consequence_changes or has_alternative_changes or condition_changed

            if needs_header:
                condition_marker = self._get_change_marker(condition_changed)
                line_txt += f"{self._get_indentation(self.scope_depth)}{condition_marker + ' ' if condition_marker else ''}#if {condition_part.get('expression', '')}\n"

                # Add consequence content if present
                if has_consequence_changes:
                    line_txt += consequence_content

                # Add #else and alternative content if present
                if has_alternative_changes:
                    line_txt += f"{self._get_indentation(self.scope_depth)}#else\n"
                    line_txt += alternative_content

                # Always close with #endif
                line_txt += f"{self._get_indentation(self.scope_depth)}#endif\n"

            return line_txt.rstrip("\n")

        elif stmt_type == "preproc_ifdef":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)

            name_part = self._get_ctrl_flow_part_obj(stmt, "name")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not name_part:
                return self._format_statement_expression(stmt, self.scope_depth)

            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""

            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) and stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_consequence_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) and stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_alternative_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            name_changed = name_part.get("modified", False) if name_part else False

            # Determine if this is #ifdef or #ifndef from the original expression
            directive_type = "#ifdef"  # default
            stmt_expression = stmt.get("expression", "")
            old_expression = stmt.get("old_expression", "")
            new_expression = stmt.get("new_expression", "")

            # Check in all expression variants for #ifndef
            if "#ifndef" in stmt_expression or "#ifndef" in old_expression or "#ifndef" in new_expression:
                directive_type = "#ifndef"

            # Determine if we need to show the header
            needs_header = has_consequence_changes or has_alternative_changes or name_changed

            if needs_header:
                name_marker = self._get_change_marker(name_changed)
                line_txt += f"{self._get_indentation(self.scope_depth)}{name_marker + ' ' if name_marker else ''}{directive_type} {name_part.get('expression', '')}\n"

                # Add consequence content if present
                if has_consequence_changes:
                    line_txt += consequence_content

                # Add #else and alternative content if present
                if has_alternative_changes:
                    line_txt += f"{self._get_indentation(self.scope_depth)}#else\n"
                    line_txt += alternative_content

                # Always close with #endif
                line_txt += f"{self._get_indentation(self.scope_depth)}#endif\n"

            return line_txt.rstrip("\n")

        elif stmt_type == "preproc_else":
            parts = stmt.get("parts", [])
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")

            # Check if there are any changes in the else content
            has_changes = False
            content = ""
            
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) or stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show if there are changes
            if has_changes:
                line_txt = f"{self._get_indentation(self.scope_depth)}#else\n"
                line_txt += content
                return line_txt.rstrip("\n")
            else:
                return ""

        elif stmt_type == "preproc_elif":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not condition_part:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""
            
            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) or stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_consequence_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) or stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_alternative_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            condition_changed = condition_part.get("modified", False) if condition_part else False

            if has_consequence_changes or condition_changed:
                condition_marker = self._get_change_marker(condition_changed)
                line_txt += f"{self._get_indentation(self.scope_depth)}{condition_marker + ' ' if condition_marker else ''}#elif {condition_part.get('expression', '')}\n"
                if has_consequence_changes:
                    line_txt += consequence_content

            if has_alternative_changes:
                line_txt += alternative_content

            return line_txt.rstrip("\n")

        elif stmt_type == "preproc_elifdef":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            name_part = self._get_ctrl_flow_part_obj(stmt, "name")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not name_part:
                return self._format_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""

            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) or stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_consequence_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                    if matches:
                        # Include if the statement is relevant to dataflow or has changes
                        if stmt_obj.get("relevant_to_dataflow", False) or stmt_obj.get("change_status", "") not in ["matched", ""]:
                            has_alternative_changes = True
                            formatted_stmt = self._format_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            name_changed = name_part.get("modified", False) if name_part else False

            if has_consequence_changes or name_changed:
                name_marker = self._get_change_marker(name_changed)
                line_txt += f"{self._get_indentation(self.scope_depth)}{name_marker + ' ' if name_marker else ''}#elifdef {name_part.get('expression', '')}\n"
                if has_consequence_changes:
                    line_txt += consequence_content

            if has_alternative_changes:
                line_txt += alternative_content

            return line_txt.rstrip("\n")


    def format_merged_statements(self, diff_format: str = "char") -> str:
        """
        Format the merged statements according to the requirements.

        Args:
            merged_statements: List of merged statement dictionaries

        Returns:
            Formatted string with diff markers and proper structure
        """
        if not self.merged_statements:
            return ""

        if diff_format not in ["char", "word"]:
            raise ValueError("Invalid diff format. Use 'char' or 'word'.")

        if diff_format == "char":
            self._diff_function = self._character_diff
        else:
            self._diff_function = self._word_diff

        # Reset processing state
        self.processed_ids = set()
        self.scope_depth = 0

        # Create a lookup dictionary for all statements
        all_statements = {stmt.get("id"): stmt for stmt in self.merged_statements if stmt.get("id")}
        
        result_lines = []

        stmt_index = 0
        
        # Find and process function definitions first
        function_statements = [stmt for stmt in self.merged_statements 
                             if stmt.get("type") == "function_definition"]
        
        if function_statements:
            result_lines.append(self._function_defitnion(function_statements[0]))
            self.processed_ids.add(function_statements[0].get("id", ""))
            self.scope_depth += 1
            stmt_index += 1
            self.scope_dict = {0: set([function_statements[0].get("id", "")])}

        # all stmt_ids where the change status is not "matched" or "relevant_to_dataflow" is True
        relevant_stmt_ids = {stmt.get("id") for stmt in self.merged_statements
                             if stmt.get("change_status") != "matched" or stmt.get("relevant_to_dataflow", False)}

        # Process all other statements
        # while stmt_index < 

        for stmt in self.merged_statements:
            stmt_id = stmt.get("id", "")
            if stmt_id in self.processed_ids:
                continue

            # Do all this recursively!

            stmt_status = stmt.get("change_status", "")
            # if stmt_status == "matched" or (stmt.get("relevant_to_dataflow", False) == False and stmt_status == "matched"):
            if stmt.get("relevant_to_dataflow", False) == False and stmt_status == "matched":
                # TODO
                # check for control flow statements, since they might be not relevant, but their inner stmt are
                continue

            is_ctrl_flow = self._is_control_flow_statement(stmt.get("type", ""))
            add_info = stmt.get("additional_info", [])

            is_struct_specifier = stmt.get("type", "") == "struct_specifier"
            is_enum_specifier = stmt.get("type", "") == "enum_specifier"
            #  and not is_struct_specifier
            if not is_ctrl_flow and not is_struct_specifier and not is_enum_specifier:
                # Format regular statements
                formatted_lines = self._format_statement_expression(stmt, self.scope_depth)
                if formatted_lines and formatted_lines.strip():
                    result_lines.extend([formatted_lines])
                self.processed_ids.add(stmt_id)
            elif is_struct_specifier:
                # Handle struct specifier statements
                # For now, just format the expression
                formatted_lines = self._format_struct_specifier_expression(stmt, self.scope_depth)
                if formatted_lines and formatted_lines.strip():
                    result_lines.append(formatted_lines)
                self.processed_ids.add(stmt_id)
            elif is_enum_specifier:
                # Handle enum specifier statements
                # For now, just format the expression
                formatted_lines = self._format_enum_specifier_expression(stmt, self.scope_depth)
                if formatted_lines and formatted_lines.strip():
                    result_lines.append(formatted_lines)
                self.processed_ids.add(stmt_id)
            else:
                # Do everthing else here
                # Handle control flow statements
                formatted_lines = self._format_ctrl_flow_stmt(stmt)
                if formatted_lines and formatted_lines.strip():
                    result_lines.append(formatted_lines)
                    # self.processed_ids.add(stmt_id)
                self.processed_ids.add(stmt_id)

                # line_txt = "text"
                # # if depth increases, add "{" or "}" as needed (in block_increase_stmts or stmt ends with "{")
                # if self._is_inc_scope(stmt.get("type", "")) or stmt.get("expression", "").endswith("{"):
                #     # Increase scope depth for control flow statements that start a block
                #     result_lines.append(f"{self._get_indentation(scope_depth)}{line_txt}{' {' if not stmt.get('type') == 'case_statement' else ':'}")
                #     scope_depth += 1
                
                # save the contained stmt ids, in the normal stmt, in new, stmt and in old stmt (in a set)
                # when we reach a stmt that doesnt have an id from that set, decrease scope depth and close the block
                # in nested blocks: keep a dic of sets for each scope depth


                # save all the statement_ids from each relevant part from the new and old statement as set (if exists), else only the normal
                # got though the statements further until next stmt not in that set anymore and save every stmt that has changed or is relevant
                # Do this recursively for nested control flow statements
                # pass

        # Add closing brace for function if needed
        if function_statements:
            result_lines.append("}")
        
        # Remove trailing empty lines
        while result_lines and not result_lines[-1].strip():
            result_lines.pop()

        # clean all empty lines
        final_lines = "\n".join(result_lines)
        result_lines = self._combine_braces_and_remove_empty(final_lines)
        # result_lines = [line for line in final_lines.splitlines() if line.strip()]  
        
        # return "\n".join(self._combine_braces(result_lines))
        # print(result_lines)
        return result_lines
    
    
    def format_from_file(self, input_file: str, output_file: str = None, diff_format: str = "char") -> str:
        """
        Format merged statements from a JSON file.
        
        Args:
            input_file: Path to input JSON file containing merged statements
            output_file: Optional path to save formatted output
            
        Returns:
            Formatted string
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                merged_statements = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error reading input file {input_file}: {e}")
        
        self.merged_statements = merged_statements if isinstance(merged_statements, list) else []
        formatted_result = self.format_merged_statements(diff_format=diff_format)
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(formatted_result)
            except IOError as e:
                raise ValueError(f"Error writing to output file {output_file}: {e}")
        
        return formatted_result

    def format_git_from_file(self, input_file: str, output_file: str = None) -> str:
        """
        Format merged statements from a JSON file in git diff style.
        
        Args:
            input_file: Path to input JSON file containing merged statements
            output_file: Optional path to save formatted output
            
        Returns:
            Formatted string in git diff style
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                merged_statements = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error reading input file {input_file}: {e}")
        
        self.merged_statements = merged_statements if isinstance(merged_statements, list) else []
        formatted_result = self.format_git_diff_style()
        
        if output_file:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(formatted_result)
            except IOError as e:
                raise ValueError(f"Error writing to output file {output_file}: {e}")
        
        return formatted_result

    def _get_git_change_marker(self, change_status: any) -> str:
        """Get the appropriate git diff marker for a change status."""
        # Handle boolean modified flags
        if isinstance(change_status, bool):
            return "" if not change_status else ""

        # Handle string change status values - only + and - for git style
        markers = {
            "inserted": "+",
            "deleted": "-",
            "changed": "",  # Will be handled specially (old line with -, new line with +)
            "moved": "+",   # Treat moved as addition at new position
            "moved_from": "-",  # Ghost showing where moved statement came from
            "modified": ""  # Will be handled specially
        }
        return markers.get(change_status, "")

    def _git_diff(self, old: str, new: str) -> str:
        """
        Git diff function that returns the new expression for git diff style.
        In git diff, modifications are handled as separate - and + lines,
        so we just return the new expression here.
        """
        if not old and not new:
            return ""
        
        if not old:
            return new if new.strip() else ""
        
        if not new:
            return ""  # For deletions, this will be handled by the calling function
        
        # For git diff style, we don't create inline diffs
        # The calling function will handle showing both old and new lines
        return new

    def _format_git_statement_expression(self, stmt: Dict[str, Any], scope_depth: int) -> str:
        """
        Format a statement expression in git diff style with + and - markers.
        Modifications are shown as deletion (-) of old line followed by addition (+) of new line.
        """
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        indentation = self._get_indentation(scope_depth)
        
        if change_status == "inserted":
            return f"{indentation}+ {expression}"
        elif change_status == "deleted":
            return f"{indentation}- {expression}"
        elif change_status == "moved_from":
            # Ghost deleted entry showing where a moved statement came from
            return f"{indentation}- {expression}"
        elif change_status == "changed" or change_status == "modified":
            # For changes, show both old and new lines
            result = ""
            if old_expression and old_expression != expression:
                result += f"{indentation}- {old_expression}\n"
            if new_expression and new_expression != old_expression:
                result += f"{indentation}+ {expression}"
            elif expression and expression != old_expression:
                result += f"{indentation}+ {expression}"
            return result.rstrip('\n') if result else f"{indentation}+ {expression}"
        elif change_status == "moved":
            # Moved statement at its new position (shown with +)
            # The ghost deleted entry shows where it was (with -)
            return f"{indentation}+ {expression}"
        else:
            # No change marker for unchanged statements
            return f"{indentation}  {expression}"

    def _format_git_ctrl_flow_part(self, part_obj: Dict[str, Any], directive_name: str, scope_depth: int) -> str:
        """
        Format a control flow part in git diff style.
        """
        if not part_obj:
            return ""
            
        modified = part_obj.get("modified", False)
        expression = part_obj.get("expression", "")
        
        indentation = self._get_indentation(scope_depth)
        
        if isinstance(modified, bool) and modified:
            # For modifications, we need to handle them as git-style changes
            # Since we don't have old/new expressions here, just mark as changed
            return f"{indentation}~ {directive_name} {expression}"
        elif modified == "inserted":
            return f"{indentation}+ {directive_name} {expression}"
        elif modified == "deleted":
            return f"{indentation}- {directive_name} {expression}"
        else:
            return f"{indentation}  {directive_name} {expression}"

    def format_git_diff_style(self, diff_format: str = "char") -> str:
        """
        Format the merged statements in git diff style with + and - markers.
        This follows the same logic as format_merged_statements but outputs git-style diffs.
        Modifications are shown as deletion of old line followed by addition of new line.
        
        Args:
            diff_format: Format for diffs ('char' or 'word') - not used in git style
            
        Returns:
            Formatted string with git-style diff markers
        """
        if not self.merged_statements:
            return ""
        
        # Set the git diff function - different from standard character/word diff
        self._diff_function = self._git_diff
        
        # Reset processing state - same as original
        self.processed_ids = set()
        self.scope_depth = 0
        
        # Create a lookup dictionary for all statements
        all_statements = {stmt.get("id"): stmt for stmt in self.merged_statements if stmt.get("id")}
        
        result_lines = []
        stmt_index = 0
        
        # Find and process function definitions first - same logic as original
        function_statements = [stmt for stmt in self.merged_statements 
                             if stmt.get("type") == "function_definition"]
        
        if function_statements:
            func_stmt = function_statements[0]
            git_func_line = self._format_git_function_definition(func_stmt)
            result_lines.append(git_func_line)
            self.processed_ids.add(func_stmt.get("id", ""))
            self.scope_depth += 1
            stmt_index += 1
            self.scope_dict = {0: set([func_stmt.get("id", "")])}

        # Process all other statements - same filtering logic as original
        for stmt in self.merged_statements:
            stmt_id = stmt.get("id", "")
            if stmt_id in self.processed_ids:
                continue

            stmt_status = stmt.get("change_status", "")
            # Same filtering logic as original
            if stmt.get("relevant_to_dataflow", False) == False and stmt_status == "matched":
                continue

            is_ctrl_flow = self._is_control_flow_statement(stmt.get("type", ""))
            stmt_type = stmt.get("type", "")
            
            is_struct_specifier = stmt_type == "struct_specifier"
            is_enum_specifier = stmt_type == "enum_specifier"
            
            if not is_ctrl_flow and not is_struct_specifier and not is_enum_specifier:
                # Format regular statements in git style
                formatted_stmt = self._format_git_statement_expression(stmt, self.scope_depth)
                if formatted_stmt:
                    # Split multi-line results (for modifications shown as - and + lines)
                    for line in formatted_stmt.split('\n'):
                        if line.strip():
                            result_lines.append(line)
                    self.processed_ids.add(stmt_id)
            elif is_struct_specifier:
                # Handle struct specifiers in git style
                formatted_lines = self._format_git_struct_specifier_expression(stmt, self.scope_depth)
                if formatted_lines:
                    for line in formatted_lines.split('\n'):
                        if line.strip():
                            result_lines.append(line)
                    self.processed_ids.add(stmt_id)
            elif is_enum_specifier:
                # Handle enum specifiers in git style
                formatted_lines = self._format_git_enum_specifier_expression(stmt, self.scope_depth)
                if formatted_lines:
                    for line in formatted_lines.split('\n'):
                        if line.strip():
                            result_lines.append(line)
                    self.processed_ids.add(stmt_id)
            else:
                # Handle control flow statements in git style
                formatted_stmt = self._format_git_ctrl_flow_stmt(stmt)
                if formatted_stmt:
                    for line in formatted_stmt.split('\n'):
                        if line.strip():
                            result_lines.append(line)
                    self.processed_ids.add(stmt_id)

        # Add closing brace for function if needed - but use smart brace balancing
        if function_statements:
            # Don't automatically add closing brace - let _balance_git_braces handle it
            pass
        
        # Remove trailing empty lines
        while result_lines and not result_lines[-1].strip():
            result_lines.pop()

        # Apply brace balancing instead of simple combining
        final_lines = "\n".join(result_lines)
        balanced_result = self._balance_git_braces(final_lines)
        
        # For git diff format, return the balanced result directly without combining
        return balanced_result

    def _balance_git_braces(self, text: str) -> str:
        """
        Balance braces in git diff output by understanding the logical structure
        rather than just mechanically counting braces in + and - lines.
        """
        lines = text.strip().splitlines()
        result = []
        
        # Track logical structure rather than just counting braces
        logical_opening_braces = 0
        logical_closing_braces = 0
        
        # Process lines to understand the logical structure
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                result.append(lines[i])
                i += 1
                continue
            
            # Get the content without git diff marker
            content = line
            if content.startswith(('+', '-', '  ')):
                content = content[1:].strip()
            
            # Check if this is a modification (- line followed by + line with similar content)
            is_modification = False
            if (i < len(lines) - 1 and 
                line.startswith('-') and 
                lines[i + 1].strip().startswith('+')):
                
                # Check if both lines have opening braces (likely same logical construct)
                current_content = content
                next_content = lines[i + 1].strip()[1:].strip()
                
                if ('{' in current_content and '{' in next_content):
                    # This is likely a modification of the same construct
                    is_modification = True
                    
                    # Count braces only once for the logical construct
                    # Use the new version (+ line) for counting
                    logical_opening_braces += next_content.count('{')
                    logical_closing_braces += next_content.count('}')
                    
                    # Add both lines to result
                    result.append(lines[i])
                    result.append(lines[i + 1])
                    
                    # Skip the next line since we processed it
                    i += 2
                    continue
            
            if not is_modification:
                # Regular line - count braces normally
                logical_opening_braces += content.count('{')
                logical_closing_braces += content.count('}')
                result.append(lines[i])
            
            i += 1
        
        # Add missing closing braces based on logical structure
        brace_deficit = logical_opening_braces - logical_closing_braces
        for _ in range(brace_deficit):
            result.append("}")
        
        return "\n".join(result)

    def _format_git_function_definition(self, func_stmt: Dict[str, Any]) -> str:
        """Format a function definition statement in git diff style."""
        func_expr = func_stmt.get("expression", "")
        func_expr_old = func_stmt.get("old_expression", "")
        change_status = func_stmt.get("change_status", "")
        
        if func_expr_old != "" and func_expr != func_expr_old:
            # For modifications, return both lines separated by newline
            return f"- {func_expr_old}\n+ {func_expr}"
        elif change_status == "inserted":
            return f"+ {func_expr}"
        elif change_status == "deleted":
            return f"- {func_expr}"
        else:
            return f"  {func_expr}"

    def _format_git_struct_specifier_expression(self, stmt: Dict[str, Any], scope_depth: int) -> str:
        """Format a struct specifier expression in git diff style."""
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        indentation = self._get_indentation(scope_depth)

        # Get the struct name till the opening brace - same logic as original
        old_struct_name = old_expression.split("{")[0].strip() if old_expression else ""
        new_struct_name = new_expression.split("{")[0].strip() if new_expression else ""
        
        current_expression = f"{expression.split('{')[0].strip()} {{"
        
        first_line = ""
        if change_status == "inserted":
            first_line = f"{indentation}+ {current_expression}"
        elif change_status == "deleted":
            first_line = f"{indentation}- {current_expression}"
        elif change_status == "moved_from":
            # Ghost deleted entry showing where a moved struct came from
            first_line = f"{indentation}- {current_expression}"
        elif change_status == "changed":
            if old_expression and new_expression and old_expression != new_expression:
                old_expr = f"{old_struct_name} {{"
                new_expr = f"{new_struct_name} {{"
                first_line = f"{indentation}- {old_expr}\n{indentation}+ {new_expr}"
            else:
                first_line = f"{indentation}+ {current_expression}"
        elif change_status == "moved":
            first_line = f"{indentation}+ {current_expression}"
        else:
            first_line = f"{indentation}  {current_expression}"

        # Handle the body of the struct - same logic as original
        fields_stmt_ids = set()
        if stmt.get("additional_info", []):
            for info in stmt["additional_info"]:
                if info.get("info") == "contained_statements":
                    fields_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("old_statement"):
            old_stmt = stmt.get("old_statement", {})
            if old_stmt.get("additional_info", []):
                for info in old_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        fields_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("new_statement"):
            new_stmt = stmt.get("new_statement", {})
            if new_stmt.get("additional_info", []):
                for info in new_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        fields_stmt_ids.update(info.get("stmt_ids", []))

        if fields_stmt_ids:
            body_lines = []
            for stmt_obj in self.merged_statements:
                if stmt_obj.get("id") in fields_stmt_ids:
                    formatted_stmt = self._format_git_normal_stmt(stmt_obj, scope_depth + 1)
                    if formatted_stmt:
                        body_lines.append(formatted_stmt)
                    self.processed_ids.add(stmt_obj.get("id"))
            if body_lines:
                body_text = "\n".join(body_lines)
                return f"{first_line}\n{body_text}\n{indentation}  }}"
            else:
                return f"{first_line}\n{indentation}  }}"
        else:
            return f"{first_line}\n{indentation}  }}"

    def _format_git_enum_specifier_expression(self, stmt: Dict[str, Any], scope_depth: int) -> str:
        """Format an enum specifier expression in git diff style."""
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        indentation = self._get_indentation(scope_depth)

        # Get the enum name till the opening brace - same logic as original
        old_enum_name = old_expression.split("{")[0].strip() if old_expression else ""
        new_enum_name = new_expression.split("{")[0].strip() if new_expression else ""
        
        current_expression = f"{expression.split('{')[0].strip()} {{"

        first_line = ""
        if change_status == "inserted":
            first_line = f"{indentation}+ {current_expression}"
        elif change_status == "deleted":
            first_line = f"{indentation}- {current_expression}"
        elif change_status == "moved_from":
            # Ghost deleted entry showing where a moved enum came from
            first_line = f"{indentation}- {current_expression}"
        elif change_status == "changed":
            if old_expression and new_expression and old_expression != new_expression:
                old_expr = f"{old_enum_name} {{"
                new_expr = f"{new_enum_name} {{"
                first_line = f"{indentation}- {old_expr}\n{indentation}+ {new_expr}"
            else:
                first_line = f"{indentation}+ {current_expression}"
        elif change_status == "moved":
            first_line = f"{indentation}+ {current_expression}"
        else:
            first_line = f"{indentation}  {current_expression}"

        # Handle the body of the enum - same logic as original
        enum_stmt_ids = set()
        if stmt.get("additional_info", []):
            for info in stmt["additional_info"]:
                if info.get("info") == "contained_statements":
                    enum_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("old_statement"):
            old_stmt = stmt.get("old_statement", {})
            if old_stmt.get("additional_info", []):
                for info in old_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        enum_stmt_ids.update(info.get("stmt_ids", []))
        if stmt.get("new_statement"):
            new_stmt = stmt.get("new_statement", {})
            if new_stmt.get("additional_info", []):
                for info in new_stmt["additional_info"]:
                    if info.get("info") == "contained_statements":
                        enum_stmt_ids.update(info.get("stmt_ids", []))

        if enum_stmt_ids:
            body_lines = []
            for stmt_obj in self.merged_statements:
                if stmt_obj.get("id") in enum_stmt_ids:
                    formatted_stmt = self._format_git_normal_stmt(stmt_obj, scope_depth + 1)
                    if formatted_stmt:
                        body_lines.append(formatted_stmt)
                    self.processed_ids.add(stmt_obj.get("id"))
            if body_lines:
                body_text = "\n".join(body_lines)
                return f"{first_line}\n{body_text}\n{indentation}  }}"
            else:
                return f"{first_line}\n{indentation}  }}"
        else:
            return f"{first_line}\n{indentation}  }}"

    def _format_git_normal_stmt(self, stmt: Dict[str, Any], scope_depth: int = 0, force_include: bool = False) -> str:
        """Git diff version of _format_normal_stmt - matches original logic."""
        stmt_id = stmt.get("id", "")
        change_status = stmt.get("change_status", "")
        stmt_type = stmt.get("type", "")

        if stmt_id in self.processed_ids:
            return None

        # Same filtering logic as original, unless force_include is True
        if not force_include and stmt.get("relevant_to_dataflow", False) == False and change_status == "matched":
            return None
        
        # Handle struct and enum specifiers specially
        if stmt_type == "struct_specifier":
            formatted_lines = self._format_git_struct_specifier_expression(stmt, scope_depth)
            if formatted_lines:
                self.processed_ids.add(stmt_id)
                return formatted_lines
            return None
        elif stmt_type == "enum_specifier":
            formatted_lines = self._format_git_enum_specifier_expression(stmt, scope_depth)
            if formatted_lines:
                self.processed_ids.add(stmt_id)
                return formatted_lines
            return None
        
        is_ctrl_flow = self._is_control_flow_statement(stmt_type)
        if not is_ctrl_flow:
            # Format regular statements
            formatted_lines = self._format_git_statement_expression(stmt, scope_depth)
            if formatted_lines:
                self.processed_ids.add(stmt_id)
                return formatted_lines
            return None
        else:
            # Handle control flow statements separately
            self.processed_ids.add(stmt_id)
            return self._format_git_ctrl_flow_stmt(stmt)

    def _stmt_matches_target_id(self, stmt_obj: Dict[str, Any], target_id: str) -> bool:
        """
        Check if a statement matches a target ID.
        For ghost (moved_from) control flow statements, the target IDs are from the old version,
        but the merged list contains statements with new IDs. We need to check match_id and
        old_statement.id to find matching statements.
        """
        stmt_id = stmt_obj.get("id", "")
        if stmt_id == target_id:
            return True
        # Check for ghost IDs that have the target_id after the "ghost_" prefix
        if stmt_id.startswith("ghost_") and stmt_id[6:] == target_id:
            return True
        if stmt_obj.get("match_id") == target_id:
            return True
        old_stmt = stmt_obj.get("old_statement", {})
        if old_stmt and old_stmt.get("id") == target_id:
            return True
        return False

    def _format_git_ctrl_flow_stmt(self, stmt: Dict[str, Any]) -> str:
        """
        Git diff version of _format_ctrl_flow_stmt - matches original comprehensive logic.
        """
        stmt_type = stmt.get("type", "")
        change_status = stmt.get("change_status", "")
        expression = stmt.get("expression", "")
        old_expression = stmt.get("old_expression", "")
        new_expression = stmt.get("new_expression", "")

        line_txt = ""

        if self._is_inc_scope(stmt.get("type", "")) or stmt.get("expression", "").endswith("{"):
            self.scope_depth += 1

        if stmt_type == "function_definition":
            # Already handled in main function
            return ""
        elif stmt_type == "if_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            condition_part = self._get_git_ctrl_flow_part_obj(stmt, "condition")
            consequence_part = self._get_git_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_git_ctrl_flow_part_obj(stmt, "alternative")

            if not condition_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            if not consequence_part and not alternative_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            # Format condition part in git style
            text_safe = {
                "condition": "",
                "consequence": "",
                "alternative": ""
            }
            line_txt = ""

            # Handle condition - show old/new versions if modified
            if condition_part.get("modified") == "modified":
                old_expr = condition_part.get('old_expression', '')
                new_expr = condition_part.get('new_expression', '')
                text_safe["condition"] = f"{self._get_indentation(self.scope_depth - 1)}- if {old_expr} {{\n"
                text_safe["condition"] += f"{self._get_indentation(self.scope_depth - 1)}+ if {new_expr} {{\n"
            elif condition_part.get("modified") == "inserted":
                new_expr = condition_part.get('new_expression', '')
                text_safe["condition"] = f"{self._get_indentation(self.scope_depth - 1)}+ if {new_expr} {{\n"
            elif condition_part.get("modified") == "deleted":
                old_expr = condition_part.get('old_expression', '')
                text_safe["condition"] = f"{self._get_indentation(self.scope_depth - 1)}- if {old_expr} {{\n"
            elif condition_part.get("modified") == "moved":
                # Moved if_statement - show with + marker since it's at new position
                expr = condition_part.get('new_expression', '') or condition_part.get('old_expression', '')
                text_safe["condition"] = f"{self._get_indentation(self.scope_depth - 1)}+ if {expr} {{\n"
            elif condition_part.get("modified") == "moved_from":
                # Ghost deleted entry showing where a moved if_statement came from
                expr = condition_part.get('old_expression', '') or condition_part.get('new_expression', '')
                text_safe["condition"] = f"{self._get_indentation(self.scope_depth - 1)}- if {expr} {{\n"
            else:
                # Unchanged
                expr = condition_part.get('new_expression', '') or condition_part.get('old_expression', '')
                text_safe["condition"] = f"{self._get_indentation(self.scope_depth - 1)}  if {expr} {{\n"

            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                is_ghost_stmt = change_status == "moved_from"
                is_moved_stmt = change_status == "moved"
                for stmt_obj in self.merged_statements:
                    # Skip ghost statements that are only in the consequence because they're
                    # placeholders for moved statements - they'll be shown at their own position
                    # (e.g., a ghost for a statement that moved from the else clause)
                    if stmt_obj.get("change_status") == "moved_from" and stmt_obj.get("id", "").startswith("ghost_"):
                        continue
                    # For ghost/moved statements, use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in consequence_stmt_ids)
                    if matches:
                        # Use _should_include_in_body to check if statement should be included
                        should_include = self._should_include_in_body(stmt_obj, consequence_stmt_ids)
                        if is_ghost_stmt:
                            # For ghost control flow statements, format the body statements with - markers
                            expr = stmt_obj.get("expression", "")
                            indentation = self._get_indentation(self.scope_depth)
                            formatted_stmt = f"{indentation}- {expr}"
                        elif is_moved_stmt:
                            # For moved control flow statements, format the body statements with + markers
                            expr = stmt_obj.get("expression", "")
                            indentation = self._get_indentation(self.scope_depth)
                            formatted_stmt = f"{indentation}+ {expr}"
                        else:
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth, force_include=should_include)
                        if formatted_stmt:
                            text_safe["consequence"] += f"{formatted_stmt}\n"
                        # Don't add to processed_ids for ghost statements - the actual statement will be processed separately
                        if not is_ghost_stmt:
                            self.processed_ids.add(stmt_obj.get("id"))
                if text_safe["consequence"].strip() != "":
                    text_safe["consequence"] += f"{self._get_indentation(self.scope_depth - 1)}  }}"
                self.scope_depth -= 1

            if alternative_part:
                alt_modified = alternative_part.get("modified", "")
                # Determine the marker for the else clause based on its status
                if alt_modified == "deleted":
                    else_marker = "-"
                elif alt_modified == "inserted":
                    else_marker = "+"
                elif alt_modified == "moved":
                    else_marker = "+"
                elif alt_modified == "moved_from":
                    else_marker = "-"
                else:
                    else_marker = " "

                # For deleted alternative parts, don't try to show inner statements individually
                # - they may have moved to a new position (will be shown there)
                # - or they were truly deleted (would have change_status=deleted)
                # Just show the entire deleted else clause as a single deletion
                if alt_modified == "deleted":
                    old_expr = alternative_part.get("old_expression", "")
                    if old_expr:
                        text_safe["alternative"] = f"{self._get_indentation(self.scope_depth - 1)}- {old_expr}"
                        # Mark only ghost statements referenced by the deleted alternative as processed
                        # so they don't get shown separately. Moved statements (change_status="moved")
                        # should NOT be marked as processed - they need to be shown at their new position.
                        alternative_stmt_ids = alternative_part.get("statement_ids", [])
                        for stmt_obj in self.merged_statements:
                            # Only mark ghost statements as processed, not moved statements
                            if stmt_obj.get("change_status") != "moved_from":
                                continue
                            matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                            if matches:
                                self.processed_ids.add(stmt_obj.get("id"))
                    else:
                        text_safe["alternative"] = ""
                else:
                    text_safe["alternative"] = f"{self._get_indentation(self.scope_depth - 1)}{else_marker} else {{\n"
                    temp_alt = ""
                    alternative_stmt_ids = alternative_part.get("statement_ids", [])
                    # For deleted alternative parts, treat inner statements as deleted too
                    is_ghost_stmt = change_status == "moved_from"
                    is_moved_stmt = change_status == "moved"
                    for stmt_obj in self.merged_statements:
                        # For ghost/moved statements, use _stmt_matches_target_id to find matching statements
                        matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in alternative_stmt_ids)
                        if matches:
                            # Use _should_include_in_body to check if statement should be included
                            should_include = self._should_include_in_body(stmt_obj, alternative_stmt_ids)
                            if is_ghost_stmt:
                                # For ghost control flow statements, format the body statements with - markers
                                expr = stmt_obj.get("expression", "")
                                indentation = self._get_indentation(self.scope_depth)
                                formatted_stmt = f"{indentation}- {expr}"
                            elif is_moved_stmt:
                                # For moved control flow statements, format the body statements with + markers
                                expr = stmt_obj.get("expression", "")
                                indentation = self._get_indentation(self.scope_depth)
                                formatted_stmt = f"{indentation}+ {expr}"
                            else:
                                formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth, force_include=should_include)
                            if formatted_stmt:
                                temp_alt += f"{formatted_stmt}\n"
                            # Don't add to processed_ids for ghost statements
                            if not is_ghost_stmt:
                                self.processed_ids.add(stmt_obj.get("id"))
                    if temp_alt.strip() != "":
                        text_safe["alternative"] += temp_alt
                        text_safe["alternative"] += f"{self._get_indentation(self.scope_depth - 1)}{else_marker} }}"
                    else:
                        text_safe["alternative"] = ""
                self.scope_depth -= 1

            line_txt += text_safe["condition"]
            if text_safe["consequence"] != "":
                line_txt += "\n" + text_safe["consequence"]
            elif text_safe["consequence"] == "":
                line_txt += "\n  }"

            if text_safe["alternative"] != "":
                line_txt += "\n" + text_safe["alternative"]
            
            return line_txt

        elif stmt_type == "switch_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            case_stmt_ids = set()
            
            condition_part = self._get_git_ctrl_flow_part_obj(stmt, "condition")

            if not condition_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            case_parts_new = [p for p in parts if p.get("part_nname") == "case_statement"]
            for case_part in case_parts_new:
                case_stmt_ids.update(case_part.get("statement_ids", []))

            old_stmt = stmt.get("old_statement")
            if old_stmt:
                old_parts = old_stmt.get("parts", [])
                case_parts_old = [p for p in old_parts if p.get("part_nname") == "case_statement"]
                for case_part in case_parts_old:
                    case_stmt_ids.update(case_part.get("statement_ids", []))
            
            # Handle condition - show old/new versions if modified
            if condition_part.get("modified") == "modified":
                old_expr = condition_part.get('old_expression', '')
                new_expr = condition_part.get('new_expression', '')
                line_txt = f"{self._get_indentation(self.scope_depth - 1)}- switch ({old_expr}) {{\n"
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}+ switch ({new_expr}) {{\n"
            elif condition_part.get("modified") == "inserted":
                new_expr = condition_part.get('new_expression', '')
                line_txt = f"{self._get_indentation(self.scope_depth - 1)}+ switch ({new_expr}) {{\n"
            elif condition_part.get("modified") == "deleted":
                old_expr = condition_part.get('old_expression', '')
                line_txt = f"{self._get_indentation(self.scope_depth - 1)}- switch ({old_expr}) {{\n"
            elif condition_part.get("modified") == "moved":
                # Moved switch_statement - show with + marker since it's at new position
                expr = condition_part.get('new_expression', '') or condition_part.get('old_expression', '')
                line_txt = f"{self._get_indentation(self.scope_depth - 1)}+ switch ({expr}) {{\n"
            elif condition_part.get("modified") == "moved_from":
                # Ghost deleted entry showing where a moved switch_statement came from
                expr = condition_part.get('old_expression', '') or condition_part.get('new_expression', '')
                line_txt = f"{self._get_indentation(self.scope_depth - 1)}- switch ({expr}) {{\n"
            else:
                # Unchanged
                expr = condition_part.get('new_expression', '') or condition_part.get('old_expression', '')
                line_txt = f"{self._get_indentation(self.scope_depth - 1)}  switch ({expr}) {{\n"
            
            for stmt_obj in self.merged_statements:
                if stmt_obj.get("id") in case_stmt_ids:
                    formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                    if formatted_stmt:
                        line_txt += f"{formatted_stmt}\n"
                    self.processed_ids.add(stmt_obj.get("id"))
            
            line_txt += f"{self._get_indentation(self.scope_depth - 1)}  }}\n"
            self.scope_depth -= 1
            
            return line_txt.rstrip("\n")

        elif stmt_type == "for_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)

            # Use _get_git_ctrl_flow_part_obj to get proper modified/old/new expression fields
            initializer_part = self._get_git_ctrl_flow_part_obj(stmt, "initializer")
            condition_part = self._get_git_ctrl_flow_part_obj(stmt, "condition")
            update_part = self._get_git_ctrl_flow_part_obj(stmt, "update")
            body_part = self._get_git_ctrl_flow_part_obj(stmt, "body")

            # Check if the statement type itself changed (e.g., while -> for)
            old_stmt = stmt.get("old_statement", {})
            old_stmt_type = old_stmt.get("type", "")
            type_changed = old_stmt_type and old_stmt_type != stmt_type

            # Check if any part is modified
            init_modified = initializer_part.get("modified") if initializer_part else None
            cond_modified = condition_part.get("modified") if condition_part else None
            update_modified = update_part.get("modified") if update_part else None
            any_part_modified = init_modified == "modified" or cond_modified == "modified" or update_modified == "modified"

            header_txt = ""
            if type_changed:
                # Type changed (e.g., while(1) -> for(;;))
                # Show the old statement type with - marker
                old_expr = stmt.get('old_expression', '') or old_stmt.get('expression', '')
                old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}- {old_header} {{\n"
                # Add the new for header
                new_init = initializer_part.get("new_expression", "") if initializer_part else ""
                new_cond = condition_part.get("new_expression", "") if condition_part else ""
                new_update = update_part.get("new_expression", "") if update_part else ""
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}+ for ({new_init}; {new_cond}; {new_update}) {{\n"
            elif any_part_modified:
                # Some part(s) changed - show old and new versions
                old_init = initializer_part.get("old_expression", "") if initializer_part else ""
                old_cond = condition_part.get("old_expression", "") if condition_part else ""
                old_update = update_part.get("old_expression", "") if update_part else ""
                new_init = initializer_part.get("new_expression", "") if initializer_part else ""
                new_cond = condition_part.get("new_expression", "") if condition_part else ""
                new_update = update_part.get("new_expression", "") if update_part else ""
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}- for ({old_init}; {old_cond}; {old_update}) {{\n"
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}+ for ({new_init}; {new_cond}; {new_update}) {{\n"
            else:
                # No modifications - use new_expression (or old_expression as fallback)
                init_expr = (initializer_part.get("new_expression") or initializer_part.get("old_expression", "")) if initializer_part else ""
                cond_expr = (condition_part.get("new_expression") or condition_part.get("old_expression", "")) if condition_part else ""
                update_expr = (update_part.get("new_expression") or update_part.get("old_expression", "")) if update_part else ""
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}  for ({init_expr}; {cond_expr}; {update_expr}) {{\n"

            line_txt = ""

            # Format body statements
            if body_part:
                body_stmt_ids = body_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    # Use _stmt_matches_target_id to find matching statements
                    matches = any(self._stmt_matches_target_id(stmt_obj, target_id) for target_id in body_stmt_ids)
                    if matches:
                        formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            if line_txt.strip() == "":
                # If no body statements, just close the for block
                line_txt = f"{header_txt}{self._get_indentation(self.scope_depth - 1)}  }}\n"
            else:
                line_txt = header_txt + line_txt
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}  }}\n"

            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "while_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)

            condition_part = self._get_git_ctrl_flow_part_obj(stmt, "condition")
            body_part = self._get_git_ctrl_flow_part_obj(stmt, "body")

            if not condition_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)

            # Check if the statement type itself changed (e.g., for -> while)
            old_stmt = stmt.get("old_statement", {})
            old_stmt_type = old_stmt.get("type", "")
            type_changed = old_stmt_type and old_stmt_type != stmt_type

            # Handle condition - show old/new versions if modified
            header_txt = ""
            if type_changed:
                # Type changed (e.g., for(;;) -> while(1))
                # Show the old statement type with - marker
                old_expr = stmt.get('old_expression', '') or old_stmt.get('expression', '')
                # Extract just the loop header from the old expression
                if old_stmt_type == "for_statement":
                    # Try to extract just "for(...)" from the full expression
                    old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                    header_txt = f"{self._get_indentation(self.scope_depth - 1)}- {old_header} {{\n"
                else:
                    old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                    header_txt = f"{self._get_indentation(self.scope_depth - 1)}- {old_header} {{\n"
                # Add the new while header
                new_expr = condition_part.get('new_expression', '') or condition_part.get('expression', '')
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}+ while ({new_expr}) {{\n"
            elif condition_part.get("modified") == "modified":
                old_expr = condition_part.get('old_expression', '')
                new_expr = condition_part.get('new_expression', '')
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}- while ({old_expr}) {{\n"
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}+ while ({new_expr}) {{\n"
            elif condition_part.get("modified") == "inserted":
                new_expr = condition_part.get('new_expression', '')
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}+ while ({new_expr}) {{\n"
            elif condition_part.get("modified") == "deleted":
                old_expr = condition_part.get('old_expression', '')
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}- while ({old_expr}) {{\n"
            else:
                # Unchanged
                expr = condition_part.get('new_expression', '') or condition_part.get('old_expression', '')
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}  while ({expr}) {{\n"
            
            line_txt = ""

            # Format body statements
            if body_part:
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in body_part.get("statement_ids", []):
                        formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            if line_txt.strip() == "":
                # If no body statements, just close the while block
                line_txt = f"{header_txt}{self._get_indentation(self.scope_depth - 1)}  }}\n"
            else:
                line_txt = header_txt + line_txt
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}  }}\n"

            self.scope_depth -= 1
            
            return line_txt.rstrip("\n")

        elif stmt_type == "do_statement":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)

            body_part = self._get_git_ctrl_flow_part_obj(stmt, "body")
            condition_part = self._get_git_ctrl_flow_part_obj(stmt, "condition")

            if not condition_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)

            # Check if the statement type itself changed (e.g., for/while -> do-while)
            old_stmt = stmt.get("old_statement", {})
            old_stmt_type = old_stmt.get("type", "")
            type_changed = old_stmt_type and old_stmt_type != stmt_type

            header_txt = ""
            footer_txt = ""
            if type_changed:
                # Type changed - show old statement with - marker
                old_expr = stmt.get('old_expression', '') or old_stmt.get('expression', '')
                old_header = old_expr.split('{')[0].strip() if '{' in old_expr else old_expr
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}- {old_header} {{\n"
                header_txt += f"{self._get_indentation(self.scope_depth - 1)}+ do {{\n"
                cond_expr = condition_part.get('new_expression', '') or condition_part.get('expression', '')
                footer_txt = f"{self._get_indentation(self.scope_depth - 1)}  }} while ({cond_expr});\n"
            else:
                # Format do-while: body first, then condition
                header_txt = f"{self._get_indentation(self.scope_depth - 1)}  do {{\n"

            line_txt = ""

            # Format body statements
            if body_part:
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in body_part.get("statement_ids", []):
                        formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))

            if line_txt.strip() == "":
                # If no body statements, just close the do block
                line_txt = f"{header_txt}{self._get_indentation(self.scope_depth - 1)}  }}\n"
            else:
                line_txt = header_txt + line_txt

            # Handle condition/footer
            if type_changed:
                line_txt += footer_txt
            elif condition_part.get("modified") == "modified":
                old_expr = condition_part.get('old_expression', '')
                new_expr = condition_part.get('new_expression', '')
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}- }} while ({old_expr});\n"
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}+ }} while ({new_expr});\n"
            elif condition_part.get("modified") == "inserted":
                new_expr = condition_part.get('new_expression', '')
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}+ }} while ({new_expr});\n"
            elif condition_part.get("modified") == "deleted":
                old_expr = condition_part.get('old_expression', '')
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}- }} while ({old_expr});\n"
            else:
                # Unchanged
                expr = condition_part.get('new_expression', '') or condition_part.get('old_expression', '')
                line_txt += f"{self._get_indentation(self.scope_depth - 1)}  }} while ({expr});\n"

            self.scope_depth -= 1

            return line_txt.rstrip("\n")

        elif stmt_type == "case_statement":
            # Case statements are handled within switch statements
            # If we encounter one standalone, treat it as a regular statement
            change_status = stmt.get("change_status", "")

            add_info = stmt.get("additional_info", [])
            contained_stmt_ids = set()
            for info in add_info:
                if info.get("info") == "contained_statements":
                    contained_stmt_ids.update(info.get("stmt_ids", []))

            parts = stmt.get("parts", [])
            header_txt = ""
            if not parts:
                # default case statement
                value_marker = self._get_git_change_marker(change_status)
                value_marker_str = value_marker if value_marker else "  "
                header_txt = f"{self._get_indentation(self.scope_depth)}{value_marker_str} default:"
            else:
                value_part = self._get_git_ctrl_flow_part_obj(stmt, "value")
                if not value_part:
                    return self._format_git_statement_expression(stmt, self.scope_depth)
                
                # Handle value - show old/new versions if modified
                if value_part.get("modified") == "modified":
                    old_val = value_part.get('old_expression', '')
                    new_val = value_part.get('new_expression', '')
                    header_txt = f"{self._get_indentation(self.scope_depth)}- case {old_val}:\n"
                    header_txt += f"{self._get_indentation(self.scope_depth)}+ case {new_val}:"
                elif value_part.get("modified") == "inserted":
                    new_val = value_part.get('new_expression', '')
                    header_txt = f"{self._get_indentation(self.scope_depth)}+ case {new_val}:"
                elif value_part.get("modified") == "deleted":
                    old_val = value_part.get('old_expression', '')
                    header_txt = f"{self._get_indentation(self.scope_depth)}- case {old_val}:"
                else:
                    # Unchanged
                    val = value_part.get('new_expression', '') or value_part.get('old_expression', '')
                    header_txt = f"{self._get_indentation(self.scope_depth)}  case {val}:"
            
            line_txt = ""

            if contained_stmt_ids:
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in contained_stmt_ids:
                        formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth + 1)
                        if formatted_stmt:
                            line_txt += f"{formatted_stmt}\n"
                        self.processed_ids.add(stmt_obj.get("id"))
            if line_txt.strip() == "":
                # If no contained statements, just return the header
                line_txt = f"{header_txt}\n"
            else:
                line_txt = f"{header_txt}\n" + line_txt
            self.scope_depth -= 1
            
            return line_txt.rstrip("\n")

        elif stmt_type == "default_statement":
            # Default statements are handled within switch statements
            # If we encounter one standalone, treat it as a regular statement
            change_status = stmt.get("change_status", "")
            marker = self._get_git_change_marker(change_status)
            marker_str = marker if marker else "  "
            line_txt = f"{self._get_indentation(self.scope_depth)}{marker_str} default:"
            
            return line_txt

        # Handle preprocessor directives
        elif stmt_type == "preproc_if":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not condition_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""
            
            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in consequence_stmt_ids:
                        if self._should_include_in_body(stmt_obj, consequence_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                                has_consequence_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in alternative_stmt_ids:
                        if self._should_include_in_body(stmt_obj, alternative_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                                has_alternative_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            condition_changed = condition_part.get("modified", False) if condition_part else False

            # Determine if we need to show the #if header
            needs_header = has_consequence_changes or has_alternative_changes or condition_changed

            if needs_header:
                condition_marker = self._get_git_change_marker(condition_changed)
                condition_marker_str = condition_marker if condition_marker else "  "
                line_txt += f"{self._get_indentation(self.scope_depth)}{condition_marker_str} #if {condition_part.get('expression', '')}\n"

                # Add consequence content if present
                if has_consequence_changes:
                    line_txt += consequence_content

                # Add #else and alternative content if present
                if has_alternative_changes:
                    line_txt += f"{self._get_indentation(self.scope_depth)}  #else\n"
                    line_txt += alternative_content

                # Always close with #endif
                line_txt += f"{self._get_indentation(self.scope_depth)}  #endif\n"

            return line_txt.rstrip("\n")

        elif stmt_type == "preproc_ifdef":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            name_part = self._get_ctrl_flow_part_obj(stmt, "name")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not name_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""
            
            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in consequence_stmt_ids:
                        if self._should_include_in_body(stmt_obj, consequence_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                                has_consequence_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in alternative_stmt_ids:
                        if self._should_include_in_body(stmt_obj, alternative_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                                has_alternative_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            name_changed = name_part.get("modified", False) if name_part else False

            # Determine if this is #ifdef or #ifndef from the original expression
            directive_type = "#ifdef"  # default
            stmt_expression = stmt.get("expression", "")
            old_expression = stmt.get("old_expression", "")
            new_expression = stmt.get("new_expression", "")

            # Check in all expression variants for #ifndef
            if "#ifndef" in stmt_expression or "#ifndef" in old_expression or "#ifndef" in new_expression:
                directive_type = "#ifndef"

            # Determine if we need to show the header
            needs_header = has_consequence_changes or has_alternative_changes or name_changed

            if needs_header:
                name_marker = self._get_git_change_marker(name_changed)
                name_marker_str = name_marker if name_marker else "  "
                line_txt += f"{self._get_indentation(self.scope_depth)}{name_marker_str} {directive_type} {name_part.get('expression', '')}\n"

                # Add consequence content if present
                if has_consequence_changes:
                    line_txt += consequence_content

                # Add #else and alternative content if present
                if has_alternative_changes:
                    line_txt += f"{self._get_indentation(self.scope_depth)}  #else\n"
                    line_txt += alternative_content

                # Always close with #endif
                line_txt += f"{self._get_indentation(self.scope_depth)}  #endif\n"

            return line_txt.rstrip("\n")

        elif stmt_type == "preproc_else":
            parts = stmt.get("parts", [])
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")

            # Check if there are any changes in the else content
            has_changes = False
            content = ""

            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in consequence_stmt_ids:
                        if self._should_include_in_body(stmt_obj, consequence_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                content += f"{formatted_stmt}\n"
                                has_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show if there are changes
            if has_changes:
                line_txt = f"{self._get_indentation(self.scope_depth)}  #else\n"
                line_txt += content
                return line_txt.rstrip("\n")
            else:
                return ""

        elif stmt_type == "preproc_elif":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            condition_part = self._get_ctrl_flow_part_obj(stmt, "condition")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not condition_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""
            
            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in consequence_stmt_ids:
                        if self._should_include_in_body(stmt_obj, consequence_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                                has_consequence_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in alternative_stmt_ids:
                        if self._should_include_in_body(stmt_obj, alternative_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                                has_alternative_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            condition_changed = condition_part.get("modified", False) if condition_part else False
            
            if has_consequence_changes or condition_changed:
                condition_marker = self._get_git_change_marker(condition_changed)
                condition_marker_str = condition_marker if condition_marker else "  "
                line_txt += f"{self._get_indentation(self.scope_depth)}{condition_marker_str} #elif {condition_part.get('expression', '')}\n"
                if has_consequence_changes:
                    line_txt += consequence_content
            
            if has_alternative_changes:
                line_txt += alternative_content

            return line_txt.rstrip("\n")

        elif stmt_type == "preproc_elifdef":
            parts = stmt.get("parts", [])
            if not parts:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            name_part = self._get_ctrl_flow_part_obj(stmt, "name")
            consequence_part = self._get_ctrl_flow_part_obj(stmt, "consequence")
            alternative_part = self._get_ctrl_flow_part_obj(stmt, "alternative")

            if not name_part:
                return self._format_git_statement_expression(stmt, self.scope_depth)
            
            # Check what parts actually have changes and collect only changed content
            has_consequence_changes = False
            has_alternative_changes = False
            consequence_content = ""
            alternative_content = ""
            
            # Check for changes in consequence part - only include statements that are relevant
            if consequence_part:
                consequence_stmt_ids = consequence_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in consequence_stmt_ids:
                        if self._should_include_in_body(stmt_obj, consequence_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                consequence_content += f"{formatted_stmt}\n"
                                has_consequence_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Check for changes in alternative part - only include statements that are relevant
            if alternative_part:
                alternative_stmt_ids = alternative_part.get("statement_ids", [])
                for stmt_obj in self.merged_statements:
                    if stmt_obj.get("id") in alternative_stmt_ids:
                        if self._should_include_in_body(stmt_obj, alternative_stmt_ids):
                            formatted_stmt = self._format_git_normal_stmt(stmt_obj, self.scope_depth)
                            if formatted_stmt:
                                alternative_content += f"{formatted_stmt}\n"
                                has_alternative_changes = True
                        self.processed_ids.add(stmt_obj.get("id"))

            # Only show parts that have changes
            line_txt = ""
            name_changed = name_part.get("modified", False) if name_part else False
            
            if has_consequence_changes or name_changed:
                name_marker = self._get_git_change_marker(name_changed)
                name_marker_str = name_marker if name_marker else "  "
                line_txt += f"{self._get_indentation(self.scope_depth)}{name_marker_str} #elifdef {name_part.get('expression', '')}\n"
                if has_consequence_changes:
                    line_txt += consequence_content
            
            if has_alternative_changes:
                line_txt += alternative_content

            return line_txt.rstrip("\n")

        else:
            # Fallback for any other control flow types
            if change_status == "inserted":
                return f"{self._get_indentation(self.scope_depth)}+ {expression}"
            elif change_status == "deleted":
                return f"{self._get_indentation(self.scope_depth)}- {expression}"
            elif change_status == "moved_from":
                # Ghost deleted entry showing where a moved statement came from
                return f"{self._get_indentation(self.scope_depth)}- {expression}"
            elif change_status == "changed" and old_expression and old_expression != expression:
                result = f"{self._get_indentation(self.scope_depth)}- {old_expression}\n"
                result += f"{self._get_indentation(self.scope_depth)}+ {expression}"
                return result
            elif change_status == "moved":
                return f"{self._get_indentation(self.scope_depth)}+ {expression}"
            else:
                return f"{self._get_indentation(self.scope_depth)}  {expression}"

