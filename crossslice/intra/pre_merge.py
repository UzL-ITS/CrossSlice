import copy

CHANGE_PRIORITY = {
    "changed": 5,
    "deleted": 4,
    "inserted": 3,
    "moved": 2,
    "matched": 1
}

def is_contained(inner_start, inner_end, outer_start, outer_end):
    """
    Return True if the [inner_start, inner_end] range lies fully within
    [outer_start, outer_end]. All args are (line, col) tuples.
    """
    # outer_start <= inner_start
    if inner_start[0] < outer_start[0] or \
       (inner_start[0] == outer_start[0] and inner_start[1] < outer_start[1]):
        return False

    # inner_end <= outer_end
    if inner_end[0] > outer_end[0] or \
       (inner_end[0] == outer_end[0] and inner_end[1] > outer_end[1]):
        return False

    return True

def find_containing_part(inner_stmt, outer_stmt):
    """
    Which part_name of `outer_stmt` contains `inner_stmt`?
    Returns the part_name or None.
    """
    inner_start = tuple(inner_stmt['start'])
    inner_end   = tuple(inner_stmt['end'])

    for part in outer_stmt.get('parts', []):
        part_start = tuple(part['start'])
        part_end   = tuple(part['end'])
        if is_contained(inner_start, inner_end, part_start, part_end):
            # NOTE: the analyzer emits the part name under the key "part_nname"
            # (historical typo, load-bearing: formatter.py reads it too).
            return part.get('part_nname', part.get('part_name'))
    return None

def run_through_stmts(stmts):
    new_stmts = []
    n = len(stmts)

    #counter = -1
    #start_temp = { 0: { "l": None , "c": None } }
    #end_temp = { 0: { "l": None, "c": None } }

    stmt_positions = []
    for i, stmt in enumerate(stmts):
        s = stmt['start']
        e = stmt['end']

        stmt_positions.append({
            'index': i,
            'id': stmt['id'],
            'start': (int(s[0]), int(s[1])),
            'end': (int(e[0]), int(e[1])),
            'change_status': stmt.get('change_status', None)
        })

    # Build containment map: for each i, list of j wehere stmt j is inside stmt i
    containment_map = { i: [] for i in range(n) }
    for i, outer_pos in enumerate(stmt_positions):
        for j, inner_pos in enumerate(stmt_positions):
            if i == j:
                continue

            if (is_contained(inner_pos['start'], inner_pos['end'], outer_pos['start'], outer_pos['end'])):
                containment_map[i].append(j)

    # Process statements to track changes in contained statements
    for i, stmt in enumerate(stmts):
        # create copy of statement to modify
        new_stmt = copy.deepcopy(stmt)

        contained_indices = containment_map.get(i, [])

        # 1) Record contained statement IDs
        if contained_indices:
            ids = [stmts[j]['id'] for j in contained_indices]
            new_stmt.setdefault('additional_info', []).append({
                'info': 'contained_statements',
                'stmt_ids': ids
            })

        # 2) Look for inner changes
        inner_changes = []
        for j in contained_indices:
            child = stmts[j]
            cs = child.get('change_status', None)
            if cs in CHANGE_PRIORITY and CHANGE_PRIORITY[cs] > 0 and cs != 'matched':
                entry = {
                    'stmt_id': child['id'],
                    'change_type': cs,
                    'expression': child.get('expression', ''),
                }
                # If this is a control-flow node (has parts), find which part
                if new_stmt.get('parts'):
                    part_name = find_containing_part(child, new_stmt)
                    entry['in_part'] = part_name
                inner_changes.append(entry)

        if inner_changes:
            new_stmt.setdefault('additional_info', []).append({
                'info': 'inner_changes',
                'changes': inner_changes
            })

            # If not a control-flow node, bump its change_status to the highest inner change
            # Note: function_definition has empty parts list but should NOT propagate inner changes
            # because moving a statement inside a function doesn't mean the function itself moved
            control_flow_types = {'if_statement', 'switch_statement', 'for_statement',
                                  'while_statement', 'do_statement', 'function_definition'}
            is_control_flow = new_stmt.get('type') in control_flow_types or new_stmt.get('parts')

            if not is_control_flow:
                # find highest priority among inner changes
                top = max(inner_changes, key=lambda c: CHANGE_PRIORITY[c['change_type']])
                top_prio = CHANGE_PRIORITY[top['change_type']]
                own = new_stmt.get('change_status', None)
                if own:
                    if top_prio > CHANGE_PRIORITY.get(own, 0):
                        new_stmt['change_status'] = top['change_type']
                else:
                    new_stmt['change_status'] = top['change_type']

        new_stmts.append(new_stmt)

    return new_stmts