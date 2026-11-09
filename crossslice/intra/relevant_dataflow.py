def mark_statements_between_moved_positions(statements):
    """
    For moved statements, mark statements BETWEEN old and new positions as relevant
    if they use any of the same variables.

    This is important for security analysis because moving a statement past a use
    of the same variable can change program semantics.

    This function should be called on MERGED statements (after merge_statements)
    because it needs both the ghost (moved_from) and moved statements.
    """
    stmt_by_id = {s["id"]: s for s in statements}
    id_list = [s["id"] for s in statements]
    idx_by_id = {sid: i for i, sid in enumerate(id_list)}

    # Helper to get all variable NAMES
    def var_names(sid):
        stmt = stmt_by_id[sid]
        names = set()
        for v in stmt.get("left_side", []):
            if v.get("name"):
                names.add(v["name"])
        for v in stmt.get("right_side", []):
            if v.get("name"):
                names.add(v["name"])
        return names

    # Find moved pairs: (moved_from_id, moved_id)
    moved_pairs = []
    for sid, s in stmt_by_id.items():
        if s.get("change_status") == "moved":
            # Find corresponding moved_from (ghost)
            for ghost_sid, ghost_s in stmt_by_id.items():
                if ghost_s.get("change_status") == "moved_from":
                    # Check if they have matching expressions (same statement)
                    if s.get("expression") == ghost_s.get("expression"):
                        moved_pairs.append((ghost_sid, sid))
                        break

    # Mark statements between moved positions as relevant if they use same variables
    for ghost_id, moved_id in moved_pairs:
        ghost_idx = idx_by_id.get(ghost_id, -1)
        moved_idx = idx_by_id.get(moved_id, -1)
        if ghost_idx < 0 or moved_idx < 0:
            continue

        # Get all variable NAMES used by the moved statement
        # We use names instead of var_ids because ghost (old version) and moved (new version)
        # have different var_ids even for the same variable
        moved_var_names = var_names(moved_id) | var_names(ghost_id)
        if not moved_var_names:
            continue

        # Determine the range between old and new positions
        start_idx = min(ghost_idx, moved_idx)
        end_idx = max(ghost_idx, moved_idx)

        # Check all statements in between
        for between_idx in range(start_idx + 1, end_idx):
            between_id = id_list[between_idx]
            between_var_names = var_names(between_id)
            # If this statement uses any of the same variables (by name), mark it as relevant
            if between_var_names & moved_var_names:
                stmt_by_id[between_id]["relevant_to_dataflow"] = True

    return statements


def find_relevant_dataflow(statements, level=2):
    """
    Mark each statement["relevant_to_dataflow"] based on a simple def–use slice
    around the initially changed statements.

    level=1 => only initial changed statements
    level=2 => + one round of backward & forward slice
    level=3 => + two rounds, etc.
    level='all' => up to convergence
    """
    # 1) Build useful indices
    stmt_by_id = {s["id"]: s for s in statements}
    # maintain original order
    id_list = [s["id"] for s in statements]
    idx_by_id = {sid: i for i, sid in enumerate(id_list)}

    # Helper to extract var_ids from left/right
    def defs(sid):
        return {
            v["var_id"] for v in stmt_by_id[sid].get("left_side", [])
            if v.get("var_id")
        }

    def uses(sid):
        return {
            v["var_id"] for v in stmt_by_id[sid].get("right_side", [])
            if v.get("var_id")
        }

    # Helper to get all var_ids (both definitions and uses)
    def all_vars(sid):
        return defs(sid) | uses(sid)

    # 2) Initial seed: any stmt with a real change_status
    seed = {
        sid for sid, s in stmt_by_id.items()
        if (cs := s.get("change_status")) and cs != "matched"
    }

    # Keep working set of relevant IDs
    relevant = set(seed)

    # 3) Perfom slices
    def backward_slice(current_ids):
        # find any stmt *before* a seed that defines a var used in seed
        result = set()
        for sid in current_ids:
            needed = set(uses(sid)) # vars this seed uses
            idx = idx_by_id[sid] # position fo that seed in the file

            # scan statements in reverse source order
            for prev_sid in reversed(id_list[:idx]):
                d = defs(prev_sid)
                if d & needed:
                    result.add(prev_sid)
                    # now we also need whatever that statement *uses*
                    needed |= uses(prev_sid)
        return result
    
    def forward_slice(current_ids):
        # find any sttm *after* a seed that uses a var defnied by seed
        result = set()

        for sid in current_ids:
            provided = set(defs(sid))        # vars this seed defines
            idx      = idx_by_id[sid]
            
            # walk forward only from idx+1 onward
            for next_sid in id_list[idx+1:]:
                u = uses(next_sid)
                if u & provided:
                    result.add(next_sid)
                    # now we also provide whatever that statement *defines*
                    provided |= defs(next_sid)
        return result
    
    if level == "all":
        # iterate until no change
        while True:
            b = backward_slice(relevant)
            f = forward_slice(relevant)
            new_relevant = relevant | b | f
            if new_relevant == relevant:
                break
            relevant = new_relevant
    else:
        # numeric level
        L = int(level)
        for _ in range(L - 1):
            b = backward_slice(relevant)
            f = forward_slice(relevant)
            relevant |= b | f

    # 4) Propagate via control-flow part_of links:
    # Build part_id -> parent stmt_id
    part_owner = {}
    for s in statements:
        for part in s.get("parts", []):
            part_owner[part["id"]] = s["id"]

    # Build parent stmt_id -> child stmt_ids mapping for downward propagation
    parent_to_children = {}
    for s in statements:
        for info in s.get("additional_info", []):
            if isinstance(info, dict) and "part_of" in info:
                pid = info["part_of"]
                parent = part_owner.get(pid)
                if parent:
                    if parent not in parent_to_children:
                        parent_to_children[parent] = set()
                    parent_to_children[parent].add(s["id"])

    # Also build parent-child relationships from parts.statement_ids
    for s in statements:
        stmt_id = s["id"]
        for part in s.get("parts", []):
            for child_id in part.get("statement_ids", []):
                if stmt_id not in parent_to_children:
                    parent_to_children[stmt_id] = set()
                parent_to_children[stmt_id].add(child_id)

    # Iterate until no more changes (bidirectional propagation)
    changed = True
    while changed:
        changed = False
        old_relevant = set(relevant)
        
        # Upward propagation: child statements to parent control flow statements
        for s in statements:
            if s["id"] in relevant:  # If child is relevant
                for info in s.get("additional_info", []):
                    if isinstance(info, dict) and "part_of" in info:
                        pid = info["part_of"]
                        parent = part_owner.get(pid)
                        if parent and parent not in relevant:
                            relevant.add(parent)
                            changed = True

        # Downward propagation: parent control flow statements to child statements
        for parent_id in list(relevant):
            if parent_id in parent_to_children:
                for child_id in parent_to_children[parent_id]:
                    if child_id in stmt_by_id:
                        # Only propagate to children that have actual changes or are already relevant
                        child_stmt = stmt_by_id[child_id]
                        child_cs = child_stmt.get("change_status", "")
                        if child_cs and child_cs != "matched":
                            if child_id not in relevant:
                                relevant.add(child_id)
                                changed = True
    
    # 5) Finally, set the flag on each stmt
    for s in statements:
        s["relevant_to_dataflow"] = (s["id"] in relevant)

    return statements
