"""Field-sensitive definitions and uses: access paths as variables.

The scalar engine (``general_code_analyzer.walk_defs_uses_scalar``) records a
definition only when a plain identifier is assigned and turns every write
through a pointer or into a field (``*p = v``, ``s->gb.x += 1``, ``a[i] = v``)
into a use of the base variable. A def-use slice over that IR cannot connect
``memcpy(s->buf, ...)`` with a later ``init(s->buf)`` or ``*len = n`` with
``return *len``: nothing defines anything.

This engine records the same scalar entries and adds one entry per **access
path**: the base variable followed by dereferences and fields, written the way
C reads (``s->gb.x``, ``s->buf[]``, ``len[]`` for ``*len``, ``v.q``). Paths are
index-insensitive (``a[i]`` and ``a[j]`` are both ``a[]``) and alias-insensitive
(``g = &s->granules[0]`` does not make ``g->x`` a path of ``s``).

A path denotes an object; the token ``P{*}`` ("part of P") stands for every
sub-object or pointee reachable from P. The rules, for a path P with proper
prefixes Q (``s[]`` and ``s->gb`` for ``s->gb.x``; the base ``s`` itself has
no path entry, its scalar entry plays that role):

* **write of P** (assignment, compound assignment, ``++``/``--``, address or
  pointer argument of a known writer such as ``memcpy``): defines ``P`` and
  ``Q{*}`` for every proper prefix Q including the base; uses the pointer
  values read on the way (the base, every prefix followed by a dereference)
  and the index expressions.
* **read of P**: uses ``P``, ``P{*}`` and every proper prefix ``Q``.
* **bare identifier x in a value-flow position** (call argument, right-hand
  side, initializer, return): the scalar use plus ``x{*}``.

So ``s->gb.x = 1`` reaches a later read of ``s->gb.x``, of the whole
``s->gb`` (through ``s->gb{*}``) and of ``s`` passed to a call (through
``s{*}``), but not a read of ``s->last_buf``; ``memset(s, 0, n)`` defines
``s[]`` and reaches every read through ``s``; ``*len = n`` reaches
``return *len``; ``scanf("%d", &x)`` defines ``x``.

``&P`` passed to an unknown function is a read of P (``ADDRESS_ARGS_MAY_WRITE``
turns it into a write as well; off because out-parameter hubs such as
``get_bits(&s->gb, n)`` then chain every statement of a decoder together).
``sizeof``, ``alignof`` and ``offsetof`` operands produce no path entries.

Entry layout, alongside the scalar entries in ``left_side``/``right_side``::

    {"name": "s->gb.x", "var_id": "<var_id of s>[].gb.x", "scope_id": ...,
     "position_start": [r, c], "position_end": [r, c],
     "id_type": "access_path", "base": "s", "base_var_id": "<var_id of s>"}

``P{*}`` entries carry ``id_type: "access_path_part"``. Consumers that want
plain variables keep filtering on ``id_type == "variable"``; the slicer, which
intersects ``var_id`` sets, needs no change.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

DEREF = "[]"                      # component: dereference / subscript
PART = "{*}"                      # suffix: "some sub-object or pointee of"

# `&P` passed to a function that is not a known writer: read of P only
# (True: also a write of P, the out-parameter assumption)
ADDRESS_ARGS_MAY_WRITE = False

# Library calls that write through an argument: name -> written positions,
# or "N.." for every position from N on (the scanf family).
WRITER_ARGS: Dict[str, object] = {
    "memcpy": (0,), "memmove": (0,), "memset": (0,), "bzero": (0,), "bcopy": (1,),
    "wmemcpy": (0,), "wmemset": (0,), "strcpy": (0,), "strncpy": (0,), "strcat": (0,),
    "strncat": (0,), "strlcpy": (0,), "strlcat": (0,), "sprintf": (0,), "snprintf": (0,),
    "vsprintf": (0,), "vsnprintf": (0,), "fgets": (0,), "gets": (0,), "fread": (0,),
    "getline": (0, 1), "read": (1,), "pread": (1,), "recv": (1,), "recvfrom": (1,),
    "strtol": (1,), "strtoul": (1,), "strtoll": (1,), "strtoull": (1,), "strtod": (1,),
    "strtof": (1,), "scanf": "1..", "sscanf": "2..", "fscanf": "2..",
}

_WRAPPERS = ("parenthesized_expression", "cast_expression")
_NO_PATH_TYPES = ("sizeof_expression", "alignof_expression", "offsetof_expression")
_PATH_TYPES = ("field_expression", "subscript_expression", "pointer_expression")

Comp = object                     # DEREF or (".", field_name)
Path = Tuple[object, List[Comp], bool]   # (base identifier node, components, address_taken)


# ---------------------------------------------------------------------------
# syntax helpers
# ---------------------------------------------------------------------------
def _operator(node) -> Optional[str]:
    op = node.child_by_field_name("operator")
    if op is not None:
        return op.type
    for ch in node.children:
        if ch.type in ("*", "&", ".", "->"):
            return ch.type
    return None


def _unwrap(node):
    """Strip parentheses and casts: ``((T *) p)`` is ``p``."""
    while node is not None and node.type in _WRAPPERS:
        if node.type == "cast_expression":
            node = node.child_by_field_name("value")
        else:
            inner = [c for c in node.named_children if c.type != "comment"]
            if len(inner) != 1:
                return node
            node = inner[0]
    return node


def path_of(node) -> Optional[Path]:
    """The access path of an lvalue-like expression rooted at an identifier:
    (base node, components from the base outward, address_taken). None when
    the root is something else (``f()->x``, a literal). ``(*s).f`` is
    ``s->f``, ``s[0].f`` is ``s[].f``, ``&*p`` and ``*&p`` are ``p``,
    ``&a[i]`` is ``a``."""
    comps: List[Comp] = []
    addr = False
    cur = _unwrap(node)
    while cur is not None:
        t = cur.type
        if t == "identifier":
            if addr and comps and comps[-1] == DEREF:     # &(*p), &a[i]
                comps.pop()
                addr = False
            return cur, comps, addr
        if t == "field_expression":
            field = cur.child_by_field_name("field")
            if field is None:
                return None
            name = field.text.decode("utf-8")
            if _operator(cur) == "->":
                comps[:0] = [DEREF, (".", name)]
            else:
                comps[:0] = [(".", name)]
            cur = _unwrap(cur.child_by_field_name("argument"))
            continue
        if t == "subscript_expression":
            comps.insert(0, DEREF)
            cur = _unwrap(cur.child_by_field_name("argument"))
            continue
        if t == "pointer_expression":
            op = _operator(cur)
            arg = _unwrap(cur.child_by_field_name("argument"))
            if op == "*":
                comps.insert(0, DEREF)
            elif op == "&":
                if comps:
                    if comps[0] != DEREF:                 # (&x).f is not C
                        return None
                    comps.pop(0)                          # *&x, (&x)[0]
                else:
                    addr = True
            else:
                return None
            cur = arg
            continue
        return None
    return None


def render_path(base: str, comps: Sequence[Comp]) -> str:
    out, i = base, 0
    while i < len(comps):
        c = comps[i]
        if c == DEREF:
            if i + 1 < len(comps) and comps[i + 1] != DEREF:
                out += "->" + comps[i + 1][1]
                i += 2
                continue
            out += "[]"
        else:
            out += "." + c[1]
        i += 1
    return out


def _encode(comps: Sequence[Comp]) -> str:
    return "".join("[]" if c == DEREF else "." + c[1] for c in comps)


def _value_flow(id_node) -> bool:
    """A bare identifier whose value flows somewhere its contents may be read:
    call argument, right-hand side, initializer, return value."""
    cur, par = id_node, id_node.parent
    while par is not None and par.type in _WRAPPERS:
        cur, par = par, par.parent
    if par is None:
        return False
    if par.type in ("argument_list", "return_statement", "initializer_list"):
        return True
    if par.type == "assignment_expression":
        return par.child_by_field_name("right") == cur
    if par.type == "init_declarator":
        return par.child_by_field_name("value") == cur
    if par.type == "conditional_expression":
        return par.child_by_field_name("condition") != cur
    return False


def written_positions(func_name: str, nargs: int, call_role_map) -> frozenset:
    """Argument positions a call to `func_name` writes through."""
    spec = WRITER_ARGS.get(func_name)
    if spec is None:
        if call_role_map and func_name in call_role_map:
            return frozenset(range(nargs))                # the scalar engine's rule
        return frozenset()
    if isinstance(spec, str):                             # "1.."
        return frozenset(range(int(spec[:-2]), nargs))
    return frozenset(spec)


def written_target(arg) -> Optional[Tuple[Path, object, list]]:
    """The object a writer writes through argument `arg`: ``&P`` writes P, a
    pointer ``P`` (or ``P + n``) writes ``P[]``. Returns (path, the node that
    forms the pointer, the other operands of a `+`/`-`), or None."""
    a = _unwrap(arg)
    if a.type == "binary_expression" and _operator_text(a) in ("+", "-"):
        sides = [a.child_by_field_name("left"), a.child_by_field_name("right")]
        for i, side in enumerate(sides):
            found = written_target(side)
            if found is not None:
                path, ptr_node, rest = found
                return path, ptr_node, rest + [sides[1 - i]]
        return None
    p = path_of(a)
    if p is None:
        return None
    base, comps, addr = p
    if addr:
        return (base, comps, False), a, []
    return (base, comps + [DEREF], False), a, []


def _operator_text(node) -> Optional[str]:
    op = node.child_by_field_name("operator")
    return op.type if op is not None else None


# ---------------------------------------------------------------------------
# the walker
# ---------------------------------------------------------------------------
class _Ctx:
    __slots__ = ("field_role_map", "scope_manager", "stmt_scope", "call_role_map",
                 "control_flow", "seen", "defs", "uses")

    def __init__(self, field_role_map, scope_manager, stmt_scope, call_role_map,
                 control_flow, defs, uses):
        self.field_role_map = field_role_map
        self.scope_manager = scope_manager
        self.stmt_scope = stmt_scope
        self.call_role_map = call_role_map
        self.control_flow = control_flow
        self.seen = set()          # (var_id, role) of path entries already recorded
        self.defs = defs
        self.uses = uses

    # -- variables ----------------------------------------------------------
    def resolve(self, id_node):
        name = id_node.text.decode("utf-8")
        var = None
        if self.scope_manager and self.stmt_scope:
            var = self.scope_manager.resolve(name, self.stmt_scope)
        if var is None and self.scope_manager:
            var = self.scope_manager.resolve_any(name)
        if var is None:
            var = self.scope_manager.declare_global(name, id_node.id)
        return var

    def scalar(self, id_node, role, id_type):
        """The scalar engine's identifier entry, unchanged (including the
        demotion of a def whose parent is a field or pointer expression)."""
        var = self.resolve(id_node)
        sr, sc = id_node.start_point
        er, ec = id_node.end_point
        entry = {
            "name": id_node.text.decode("utf-8"),
            "position_start": [sr, sc],
            "position_end": [er, ec],
            "var_id": var.id,
            "scope_id": var.scope_id,
            "id_type": id_type,
        }
        parent_type = id_node.parent.type if getattr(id_node, "parent", None) else None
        if role == "def" and parent_type in {"field_expression", "pointer_expression"}:
            role = "use"
        (self.defs if role == "def" else self.uses).append(entry)
        return var

    # -- path entries -------------------------------------------------------
    def _add(self, role, var, base_name, comps, span, part):
        var_id = var.id + _encode(comps) + (PART if part else "")
        if (var_id, role) in self.seen:
            return
        self.seen.add((var_id, role))
        sr, sc = span.start_point
        er, ec = span.end_point
        (self.defs if role == "def" else self.uses).append({
            "name": render_path(base_name, comps) + (PART if part else ""),
            "position_start": [sr, sc],
            "position_end": [er, ec],
            "var_id": var_id,
            "scope_id": var.scope_id,
            "id_type": "access_path_part" if part else "access_path",
            "base": base_name,
            "base_var_id": var.id,
        })

    def write(self, path: Path, span):
        """Define P and `Q{*}` for every proper prefix Q, the base included."""
        base, comps, _ = path
        if not comps:                                     # `&x` to a writer: x itself
            var = self.resolve(base)
            sr, sc = base.start_point
            er, ec = base.end_point
            self.defs.append({
                "name": base.text.decode("utf-8"), "position_start": [sr, sc],
                "position_end": [er, ec], "var_id": var.id, "scope_id": var.scope_id,
                "id_type": "variable",
            })
            return
        var = self.resolve(base)
        name = base.text.decode("utf-8")
        self._add("def", var, name, comps, span, part=False)
        for k in range(len(comps)):
            self._add("def", var, name, comps[:k], span, part=True)

    def read(self, path: Path, span, part=True):
        """Use P, `P{*}` and every proper prefix with at least one component."""
        base, comps, _ = path
        if not comps:
            return
        var = self.resolve(base)
        name = base.text.decode("utf-8")
        self._add("use", var, name, comps, span, part=False)
        if part:
            self._add("use", var, name, comps, span, part=True)
        for k in range(1, len(comps)):
            self._add("use", var, name, comps[:k], span, part=False)

    def part_use(self, id_node):
        var = self.resolve(id_node)
        self._add("use", var, id_node.text.decode("utf-8"), [], id_node, part=True)

    def lvalue_reads(self, node, path: Path, id_type="variable"):
        """What computing the address of P reads: the base variable, the
        index expressions, and every prefix followed by a dereference."""
        base, comps, _ = path
        cur = _unwrap(node)
        while cur is not None and cur.type != "identifier":
            if cur.type == "subscript_expression":
                _walk(cur.child_by_field_name("index"), "use", "variable", self)
            arg = cur.child_by_field_name("argument")
            if arg is None:
                break
            cur = _unwrap(arg)
        self.scalar(base, "use", id_type)
        for k in range(1, len(comps)):
            if comps[k] == DEREF:
                self.read((base, comps[:k], False), node, part=False)


def _walk(node, role, id_type, ctx: _Ctx, paths=True):
    if node is None:
        return
    t = node.type

    if t == "identifier":
        ctx.scalar(node, role, id_type)
        if paths and role == "use" and id_type == "variable" and _value_flow(node):
            ctx.part_use(node)
        return

    if t == "call_expression" and ctx.call_role_map is not None:
        _call(node, ctx, paths)
        return

    if t == "assignment_expression":
        _assignment(node, role, id_type, ctx, paths)
        return

    if t == "update_expression":
        arg = node.child_by_field_name("argument")
        p = path_of(arg) if (paths and arg is not None) else None
        if p and p[1] and not p[2]:
            ctx.write(p, arg)
            ctx.read(p, arg)
            ctx.lvalue_reads(arg, p)
        else:
            _walk(arg, "def", id_type, ctx, paths)
            _walk(arg, "use", id_type, ctx, paths)
        _walk_rest(node, (arg,), role, id_type, ctx, paths)
        return

    if t == "return_statement":
        for child in node.named_children:
            _walk(child, "use", id_type, ctx, paths)
        return

    if paths and t in _PATH_TYPES:
        if _path_node(node, role, id_type, ctx):
            return

    if t in _NO_PATH_TYPES:
        paths = False

    mapping = ctx.field_role_map.get(t, {})
    visited = set()
    for field_name in mapping.get("def", []):
        child = node.child_by_field_name(field_name)
        if child:
            visited.add(child.id)
            _walk(child, "def", id_type, ctx, paths)
    for field_name in mapping.get("use", []):
        child = node.child_by_field_name(field_name)
        if child:
            visited.add(child.id)
            _walk(child, "use", id_type, ctx, paths)
    if t in ctx.control_flow:
        return
    for child in node.named_children:
        if child.id not in visited:
            _walk(child, role, id_type, ctx, paths)


def _path_node(node, role, id_type, ctx: _Ctx) -> bool:
    """A field, subscript or pointer expression; False when it has no path
    (root is a call or literal) and the generic mapping should handle it."""
    p = path_of(node)
    if p is None:
        return False
    base, comps, addr = p
    if not comps:                                       # &x, *&x, &a[i]: the variable itself
        if addr:
            ctx.scalar(base, "use", id_type)
            if role == "use" and id_type == "variable":
                ctx.part_use(base)                      # &x to a call: its contents may be read
                if ADDRESS_ARGS_MAY_WRITE and _value_flow(node):
                    ctx.write((base, [], False), node)
        elif role == "def":
            ctx.lvalue_reads(node, p, id_type)
            ctx.scalar(base, "def", id_type)
        else:
            ctx.lvalue_reads(node, p, id_type)          # the base and the index expressions
            if id_type == "variable" and _value_flow(node):
                ctx.part_use(base)                      # &a[i] passed on: a's contents may be read
        return True
    if role == "def" and not addr:
        ctx.write(p, node)
    else:
        ctx.read(p, node)
        if addr and ADDRESS_ARGS_MAY_WRITE and role == "use" and _value_flow(node):
            ctx.write(p, node)
    ctx.lvalue_reads(node, p, id_type)
    return True


def _assignment(node, role, id_type, ctx: _Ctx, paths):
    from crossslice.intra.general_code_analyzer import is_compound_assignment
    left = node.child_by_field_name("left")
    right = node.child_by_field_name("right")
    compound = is_compound_assignment(node)
    p = path_of(left) if (paths and left is not None) else None
    if p and p[1] and not p[2]:
        ctx.write(p, left)
        if compound:
            ctx.read(p, left)
        ctx.lvalue_reads(left, p)
    elif left is not None:
        _walk(left, "def", id_type, ctx, paths)
        if compound:
            _walk(left, "use", id_type, ctx, paths)
    _walk(right, "use", id_type, ctx, paths)
    _walk_rest(node, (left, right), role, id_type, ctx, paths)


def _walk_rest(node, handled, role, id_type, ctx: _Ctx, paths):
    """The named children that are not fields of the node: what tree-sitter's
    error recovery attaches to a statement (`MACRO(x) i++;` puts `i` into an
    ERROR node), walked with the inherited role as the scalar engine does."""
    skip = {c.id for c in handled if c is not None}
    for child in node.named_children:
        if child.id not in skip:
            _walk(child, role, id_type, ctx, paths)


def _call(node, ctx: _Ctx, paths):
    from crossslice.intra.general_code_analyzer import clean_string, is_valid_argument_node
    fn_node = node.child_by_field_name("function")
    func_name = ""
    if fn_node is not None and fn_node.type == "identifier":
        func_name = fn_node.text.decode("utf-8")
    elif fn_node is not None:
        func_name = clean_string(fn_node.text.decode("utf-8"))
    if fn_node is not None:
        _walk(fn_node, "use", "function_call", ctx, paths)

    args_node = node.child_by_field_name("arguments")
    if args_node is None:
        return
    args = [a for a in args_node.children if is_valid_argument_node(a) and a.type != "comment"]
    written = written_positions(func_name, len(args), ctx.call_role_map)
    for i, arg in enumerate(args):
        target = written_target(arg) if (paths and i in written) else None
        if target is not None:
            path, ptr_node, rest = target
            ctx.write(path, ptr_node)
            base, comps, _ = path
            p = _unwrap(ptr_node)
            if p.type == "pointer_expression" and _operator(p) == "&":
                if comps:                                 # &s->gb: s is read; &x: nothing
                    ctx.lvalue_reads(p.child_by_field_name("argument"), path)
            else:                                         # a pointer: its value is read
                ctx.read((base, comps[:-1], False), ptr_node, part=False)
                ctx.lvalue_reads(ptr_node, (base, comps[:-1], False))
            for other in rest:                            # the offset in `p + n`
                _walk(other, "use", "variable", ctx, paths)
        elif i in written:
            _walk(arg, "def", "variable", ctx, paths)      # the scalar engine's rule
        else:
            _walk(arg, "use", "variable", ctx, paths)


def walk_defs_uses_fields(node, field_role_map, defs_out, uses_out, role="use",
                          scope_manager=None, stmt_scope=None, call_role_map=None,
                          id_type_str="variable"):
    """Drop-in replacement for ``walk_defs_uses_scalar`` with the same
    signature: records the scalar entries and the access-path entries
    described in the module docstring."""
    from crossslice.intra.general_code_analyzer import ctf_mapping
    ctx = _Ctx(field_role_map, scope_manager, stmt_scope, call_role_map,
               set(ctf_mapping.get("control_flow_types", [])), defs_out, uses_out)
    _walk(node, role, id_type_str, ctx)


def path_entries(stmt: dict, side: str = "left_side") -> List[dict]:
    """The access-path entries (not the part tokens) of one side of a statement."""
    return [v for v in stmt.get(side, []) if v.get("id_type") == "access_path"]
