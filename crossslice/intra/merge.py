import json
from collections import OrderedDict, defaultdict
from typing import List, Dict, Any, Tuple, Optional

from crossslice.intra.variable_mapping_during_merge import create_variable_mapping_during_merge


def load_statements(path: str) -> List[Dict[str, Any]]:
    with open(path, 'r') as f:
        return json.load(f)

def build_id_maps(stmts: List[Dict[str, Any]]) -> Tuple[Dict[str, Dict], Dict[str, int]]:
    """Build id->statement and id->index maps"""
    id_map = {}
    idx_map = {}
    for idx, stmt in enumerate(stmts):
        id_map[stmt['id']] = stmt
        idx_map[stmt['id']] = idx
    return id_map, idx_map

def build_match_map(stmts: List[Dict[str, Any]]) -> Dict[str, str]:
    """Returns {id: match_id} for all statements with a match_id."""
    match_map = {}
    for stmt in stmts:
        if 'match_id' in stmt and stmt['match_id']:
            match_map[stmt['id']] = stmt['match_id']
    return match_map

def build_part_of_map(stmts: List[Dict[str, Any]]) -> Dict[str, str]:
    """Returns {id: parent_id} for statements that are part of another statement."""
    part_of_map = {}
    for stmt in stmts:
        for info in stmt.get('additional_info', []):
            if isinstance(info, dict) and info.get('part_of'):
                part_of_map[stmt['id']] = info['part_of']
                break
    return part_of_map

def build_statement_order_map(stmts: List[Dict[str, Any]]) -> List[str]:
    """Build ordered list of statement IDs as they appear in the file"""
    return [stmt['id'] for stmt in stmts]

def find_control_flow_parent(stmt_id: str, part_of_map: Dict[str, str],
                           old_stmts_map: Dict[str, Dict], new_stmts_map: Dict[str, Dict]) -> Optional[str]:
    """
    Find the control flow statement that contains this statement.
    Returns the ID of the parent control flow statement (if_statement, etc.)
    """
    if stmt_id not in part_of_map:
        return None

    parent_part_id = part_of_map[stmt_id]

    # Look through all statements to find which one contains this part
    for stmt_id_candidate, stmt in old_stmts_map.items():
        if stmt.get('type') in ['if_statement', 'switch_statement', 'for_statement', 'while_statement', 'do_statement', 'function_definition']:
            for part in stmt.get('parts', []):
                if part.get('id') == parent_part_id:
                    return stmt_id_candidate

        if stmt.get('old_statement', {}):
            if stmt['old_statement'].get('id') == parent_part_id:
                return stmt_id_candidate
            # if not found, check the parts
            parts = stmt.get('old_statement', {}).get('parts', [])
            for part in parts:
                if part.get('id') == parent_part_id:
                    return stmt_id_candidate

    # Also check new statements
    for stmt_id_candidate, stmt in new_stmts_map.items():
        if stmt.get('type') in ['if_statement', 'switch_statement', 'for_statement', 'while_statement', 'do_statement', 'function_definition']:
            for part in stmt.get('parts', []):
                if part.get('id') == parent_part_id:
                    return stmt_id_candidate

        if stmt.get('new_statement', {}):
            if stmt['new_statement'].get('id') == parent_part_id:
                return stmt_id_candidate
            # if not found, check the parts
            parts = stmt.get('new_statement', {}).get('parts', [])
            for part in parts:
                if part.get('id') == parent_part_id:
                    return stmt_id_candidate

    return None


def find_control_flow_block_end(cf_stmt_idx: int, merged: List[Dict[str, Any]]) -> int:
    """
    Find the index of the last statement that belongs to a control flow block.

    When a control flow statement (like if_statement) is at index cf_stmt_idx in merged,
    this function finds the last statement that is contained within that block
    (i.e., has a higher scope level and comes right after it).

    Returns the index of the last statement in the block, or cf_stmt_idx if no
    contained statements are found.
    """
    if cf_stmt_idx >= len(merged):
        return cf_stmt_idx

    cf_stmt = merged[cf_stmt_idx]
    cf_scope = cf_stmt.get('scope_level', 0)
    cf_type = cf_stmt.get('type', '')

    # Only process control flow statements
    if cf_type not in ['if_statement', 'switch_statement', 'for_statement',
                        'while_statement', 'do_statement', 'preproc_if']:
        return cf_stmt_idx

    # Find all statements that are inside this control flow block
    # They will have scope_level > cf_scope and come immediately after
    last_contained_idx = cf_stmt_idx

    for i in range(cf_stmt_idx + 1, len(merged)):
        stmt = merged[i]
        stmt_scope = stmt.get('scope_level', 0)

        # If we hit a statement at the same or lower scope level, we've exited the block
        if stmt_scope <= cf_scope:
            break

        # This statement is inside the control flow block
        last_contained_idx = i

    return last_contained_idx


def find_parent_with_part_containing_stmt(stmt_id: str, stmts: List[Dict[str, Any]]) -> Optional[Tuple[str, Dict]]:
    """
    Find the IMMEDIATE parent control flow statement and the specific part that contains stmt_id.
    Returns (parent_stmt_id, part_dict) or None if not found.

    This searches through all statements' parts to find which one has stmt_id in its statement_ids.
    Also checks additional_info for contained_statements (used by case_statement).
    Since statements can be nested, we need to find the MOST SPECIFIC (deepest) parent,
    which is the one with the smallest statement_ids list containing our target.
    """
    best_match = None
    smallest_size = float('inf')

    for stmt in stmts:
        # Check parts[].statement_ids (standard control flow structures)
        for part in stmt.get('parts', []):
            stmt_ids = part.get('statement_ids', [])
            if stmt_id in stmt_ids:
                # Prefer the parent with the smallest statement_ids list
                # (more specific/deeper nesting)
                if len(stmt_ids) < smallest_size:
                    smallest_size = len(stmt_ids)
                    best_match = (stmt['id'], part)

        # Also check additional_info for contained_statements (used by case_statement)
        for info in stmt.get('additional_info', []):
            if info.get('info') == 'contained_statements':
                stmt_ids = info.get('stmt_ids', [])
                if stmt_id in stmt_ids:
                    if len(stmt_ids) < smallest_size:
                        smallest_size = len(stmt_ids)
                        # Return the info dict as the "part" so ghost can be added to it
                        best_match = (stmt['id'], info)

    return best_match

def find_insertion_position(deleted_stmt_id: str, old_order: List[str], merged_ids: List[str], merged_stmts: List[Dict[str, Any]]) -> int:
    """
    Find the best position to insert a deleted statement based on surrounding context.
    Returns the index where the statement should be inserted in the merged list.
    """
    if deleted_stmt_id not in old_order:
        return len(merged_ids)  # Append at end if not found
    
    old_idx = old_order.index(deleted_stmt_id)

    # print(f"Finding position for deleted statement {deleted_stmt_id} at old index {old_idx} in old order.")
    
    # Create maps for efficient lookup
    merged_id_to_idx = {stmt_id: i for i, stmt_id in enumerate(merged_ids)}
    merged_id_to_status = {merged_ids[i]: merged_stmts[i].get('change_status', '') for i in range(len(merged_ids))}
    
    # Create a map of old statement IDs to merged statement positions via match_id
    old_id_to_merged_pos = {}
    for i, merged_stmt in enumerate(merged_stmts):
        match_id = merged_stmt.get('match_id')
        if match_id:
            old_id_to_merged_pos[match_id] = i
        # Also check old_statement for changed statements
        old_stmt = merged_stmt.get('old_statement', {})
        if old_stmt and old_stmt.get('id'):
            old_id_to_merged_pos[old_stmt['id']] = i
    
    # First pass: Look for nearest neighbors in old_order that have matches in merged
    # Search both directions simultaneously to find the closest match
    max_distance = max(old_idx, len(old_order) - old_idx - 1)
    
    for distance in range(1, max_distance + 1):
        # Check statement after current position
        next_idx = old_idx + distance
        if next_idx < len(old_order):
            next_stmt_id = old_order[next_idx]
            if next_stmt_id in old_id_to_merged_pos:
                merged_pos = old_id_to_merged_pos[next_stmt_id]
                if merged_id_to_status.get(merged_ids[merged_pos], '') != 'deleted':
                    # Insert before this non-deleted statement
                    return merged_pos
        
        # Check statement before current position
        prev_idx = old_idx - distance
        if prev_idx >= 0:
            prev_stmt_id = old_order[prev_idx]
            if prev_stmt_id in old_id_to_merged_pos:
                merged_pos = old_id_to_merged_pos[prev_stmt_id]
                if merged_id_to_status.get(merged_ids[merged_pos], '') != 'deleted':
                    # Insert after this non-deleted statement
                    return merged_pos + 1
    
    # Second pass: If no matches via match_id, look for direct matches in merged_ids
    # (These would be new statement IDs that happen to be in old_order - edge case)
    for distance in range(1, max_distance + 1):
        # Check statement after current position
        next_idx = old_idx + distance
        if next_idx < len(old_order):
            next_stmt_id = old_order[next_idx]
            if next_stmt_id in merged_id_to_idx and merged_id_to_status.get(next_stmt_id, '') != 'deleted':
                # Insert before this non-deleted statement
                return merged_id_to_idx[next_stmt_id]
        
        # Check statement before current position
        prev_idx = old_idx - distance
        if prev_idx >= 0:
            prev_stmt_id = old_order[prev_idx]
            if prev_stmt_id in merged_id_to_idx and merged_id_to_status.get(prev_stmt_id, '') != 'deleted':
                # Insert after this non-deleted statement
                return merged_id_to_idx[prev_stmt_id] + 1
    
    # Third pass: Fall back to any neighbors (including deleted statements)
    for distance in range(1, max_distance + 1):
        # Check statement after current position
        next_idx = old_idx + distance
        if next_idx < len(old_order):
            next_stmt_id = old_order[next_idx]
            if next_stmt_id in old_id_to_merged_pos:
                # Insert before this statement
                return old_id_to_merged_pos[next_stmt_id]
            if next_stmt_id in merged_id_to_idx:
                # Insert before this statement
                return merged_id_to_idx[next_stmt_id]
        
        # Check statement before current position
        prev_idx = old_idx - distance
        if prev_idx >= 0:
            prev_stmt_id = old_order[prev_idx]
            if prev_stmt_id in old_id_to_merged_pos:
                # Insert after this statement
                return old_id_to_merged_pos[prev_stmt_id] + 1
            if prev_stmt_id in merged_id_to_idx:
                # Insert after this statement
                return merged_id_to_idx[prev_stmt_id] + 1
    
    # If no neighbors found, append at end
    print(f"No neighbors found for {deleted_stmt_id}, appending at end")
    return len(merged_ids)

def find_insertion_position_in_control_flow(deleted_stmt_id: str, old_order: List[str], 
                                           merged_ids: List[str], merged_stmts: List[Dict[str, Any]],
                                           parent_cf_stmt: Dict[str, Any], parent_idx: int,
                                           old_part_of_map: Dict[str, str]) -> int:
    """
    Find insertion position for a deleted statement within a specific control flow structure.
    Only considers neighbors that belong to the same control flow structure.
    """
    if deleted_stmt_id not in old_order:
        return parent_idx + 1  # Insert right after the control flow statement
    
    old_idx = old_order.index(deleted_stmt_id)
    
    # Get the part_of ID for this deleted statement
    deleted_part_of = old_part_of_map.get(deleted_stmt_id)
    if not deleted_part_of:
        return parent_idx + 1
    
    # Create maps for efficient lookup
    merged_id_to_idx = {stmt_id: i for i, stmt_id in enumerate(merged_ids)}
    merged_id_to_status = {merged_ids[i]: merged_stmts[i].get('change_status', '') for i in range(len(merged_ids))}
    
    # Create a map of old statement IDs to merged statement positions via match_id
    old_id_to_merged_pos = {}
    for i, merged_stmt in enumerate(merged_stmts):
        match_id = merged_stmt.get('match_id')
        if match_id:
            old_id_to_merged_pos[match_id] = i
        # Also check old_statement for changed statements
        old_stmt = merged_stmt.get('old_statement', {})
        if old_stmt and old_stmt.get('id'):
            old_id_to_merged_pos[old_stmt['id']] = i
    
    # Find all statements that belong to the same control flow part
    same_part_neighbors = []
    
    for stmt_id in old_order:
        if stmt_id == deleted_stmt_id:
            continue
        
        # Check if this statement belongs to the same part of the control flow
        stmt_part_of = old_part_of_map.get(stmt_id)
        if stmt_part_of == deleted_part_of:
            # This statement is in the same part, check if it's in merged
            if stmt_id in old_id_to_merged_pos:
                merged_pos = old_id_to_merged_pos[stmt_id]
                old_stmt_idx = old_order.index(stmt_id)
                same_part_neighbors.append((old_stmt_idx, merged_pos, stmt_id))
    
    if not same_part_neighbors:
        # No neighbors in the same part, insert right after the control flow statement
        return parent_idx + 1
    
    # Sort by old order position
    same_part_neighbors.sort(key=lambda x: x[0])
    
    # Find the best insertion position relative to neighbors in the same part
    for old_neighbor_idx, merged_pos, neighbor_id in same_part_neighbors:
        if old_neighbor_idx > old_idx:
            # This neighbor comes after the deleted statement in old order
            # Insert before it if it's not deleted
            if merged_id_to_status.get(merged_ids[merged_pos], '') != 'deleted':
                return merged_pos
    
    # If no neighbor found after, look for one before and insert after it
    for old_neighbor_idx, merged_pos, neighbor_id in reversed(same_part_neighbors):
        if old_neighbor_idx < old_idx:
            # This neighbor comes before the deleted statement in old order
            # Insert after it if it's not deleted
            if merged_id_to_status.get(merged_ids[merged_pos], '') != 'deleted':
                return merged_pos + 1
    
    # Fallback: insert right after the control flow statement
    return parent_idx + 1

def insert_deleted_statement_in_control_flow(deleted_stmt: Dict[str, Any], 
                                           control_flow_stmt: Dict[str, Any],
                                           part_of_map: Dict[str, str]) -> bool:
    """
    Try to insert a deleted statement into the appropriate part of a control flow statement.
    Returns True if successfully inserted, False otherwise.
    """
    deleted_id = deleted_stmt['id']
    if deleted_id not in part_of_map:
        return False
    
    target_part_id = part_of_map[deleted_id]
    
    # Find the matching part in the control flow statement
    for part in control_flow_stmt.get('parts', []):
        if part.get('id') == target_part_id:
            # Add to statement_ids if not already there
            if 'statement_ids' not in part:
                part['statement_ids'] = []
            if deleted_id not in part['statement_ids']:
                part['statement_ids'].append(deleted_id)
            return True
    
    return False

def detect_order_changes(match_pairs: List[Tuple[str, str]],
                         old_idx_map: Dict[str, int],
                         new_idx_map: Dict[str, int],
                         old_id_map: Dict[str, Dict],
                         new_id_map: Dict[str, Dict]) -> set:
    """
    Detect statements that GumTree has identified as moved.

    This function now trusts GumTree's move-tree detection rather than trying to
    infer movements from relative order changes. A statement is only marked as
    moved if:
    1. GumTree already marked it as "moved" via matching.py
    2. OR its scope_level actually changed (moved between scopes)

    The second condition handles edge cases where scope changes might not be
    captured by GumTree's move-tree action.

    Returns:
        Set of old statement IDs that have moved.
    """
    if len(match_pairs) < 2:
        return set()

    moved_ids = set()

    for old_id, new_id in match_pairs:
        old_stmt = old_id_map.get(old_id, {})
        new_stmt = new_id_map.get(new_id, {})

        # If GumTree already marked this as moved, trust it
        if old_stmt.get('change_status') == 'moved' or new_stmt.get('change_status') == 'moved':
            moved_ids.add(old_id)
            continue

        # Also detect scope level changes as moves
        # This catches cases where a statement moved between scopes
        old_scope_level = old_stmt.get('scope_level', 0)
        new_scope_level = new_stmt.get('scope_level', 0)

        if old_scope_level != new_scope_level:
            moved_ids.add(old_id)

    return moved_ids


def merge_statements(old_stmts: List[Dict[str, Any]], new_stmts: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, str]]:
    """
    Merge old and new statements and create variable mapping.

    Returns:
        Tuple of (merged_statements, variable_mapping)
    """
    if not old_stmts:
        for s in new_stmts:
            s['change_status'] = s.get('change_status', 'inserted')
            s['relevant_to_dataflow'] = True
        # Create variable mapping for new statements only
        var_mapping = create_variable_mapping_during_merge([], new_stmts, [])
        return list(new_stmts), var_mapping
    if not new_stmts:
        for s in old_stmts:
            s['change_status'] = s.get('change_status', 'deleted')
            s['relevant_to_dataflow'] = True
        # Create variable mapping for old statements only
        var_mapping = create_variable_mapping_during_merge(old_stmts, [], [])
        return list(old_stmts), var_mapping
    
    # Build all necessary mappings
    old_id_map, old_idx_map = build_id_maps(old_stmts) # id_map[stmt['id']] = stmt
    new_id_map, new_idx_map = build_id_maps(new_stmts) # dx_map[stmt['id']] = idx
    old_match_map = build_match_map(old_stmts)
    new_match_map = build_match_map(new_stmts)
    old_part_of_map = build_part_of_map(old_stmts) # {id: parent_id}
    new_part_of_map = build_part_of_map(new_stmts) # {id: parent_id}
    old_order = build_statement_order_map(old_stmts)
    new_order = build_statement_order_map(new_stmts)

    # Track processed statements
    processed_old = set()
    processed_new = set()
    merged = []
    merged_ids = []  # Track IDs for position finding

    # Step 1: Process matched statements in new code order
    match_pairs = []
    for old in old_stmts:
        if 'match_id' in old and old['match_id']:
            new_id = old['match_id']
            if new_id in new_id_map:
                match_pairs.append((old['id'], new_id))

    # Sort by new code order
    match_pairs.sort(key=lambda p: new_idx_map.get(p[1], 1e9))

    # Detect order changes: find statements whose relative position changed
    # A statement is "moved" if its scope_level changed or its relative order
    # with respect to other matched statements at the same scope level changed
    moved_old_ids = detect_order_changes(match_pairs, old_idx_map, new_idx_map, old_id_map, new_id_map)

    # merge matched statements first, in new code order
    for old_id, new_id in match_pairs:
        old_stmt = old_id_map[old_id]
        new_stmt = new_id_map[new_id]
        processed_old.add(old_id)
        processed_new.add(new_id)

        # Create merged statement
        merged_stmt = dict(new_stmt)
        if (old_stmt['type'] != new_stmt['type'] or
            old_stmt.get('expression') != new_stmt.get('expression') or
            old_stmt.get('change_status') == 'changed' or
            new_stmt.get('change_status') == 'changed'):
            merged_stmt['change_status'] = 'changed'
            merged_stmt['old_expression'] = old_stmt.get('expression', '')
            merged_stmt['new_expression'] = new_stmt.get('expression', '')
            merged_stmt['old_statement'] = old_stmt
            merged_stmt['new_statement'] = new_stmt
        elif old_id in moved_old_ids:
            # Same expression, but scope/position changed - mark as moved
            merged_stmt['change_status'] = 'moved'
            merged_stmt['old_statement'] = old_stmt
            merged_stmt['new_statement'] = new_stmt
        else:
            merged_stmt['change_status'] = 'matched'

        merged.append(merged_stmt)
        merged_ids.append(new_id)

    # Step 2: Insert new-only statements (inserted) in their natural positions
    for new_stmt in new_stmts:
        if new_stmt['id'] not in processed_new and (not new_stmt.get('match_id')):
            stmt = dict(new_stmt)
            stmt['change_status'] = stmt.get('change_status', 'inserted')
            if stmt['change_status'] in ('changed', 'moved'):
                # no counterpart in the old version (the matcher dropped its match)
                stmt['change_status'] = 'inserted'
            
            # Find position based on new code order
            new_pos = new_idx_map[new_stmt['id']]
            insert_pos = 0
            
            # Find where to insert based on already merged statements
            for i, merged_id in enumerate(merged_ids):
                if new_idx_map.get(merged_id, 1e9) > new_pos:
                    insert_pos = i
                    break
                insert_pos = i + 1
            
            merged.insert(insert_pos, stmt)
            merged_ids.insert(insert_pos, new_stmt['id'])
            processed_new.add(new_stmt['id'])

    # Step 3: Handle deleted statements with intelligent positioning
    deleted_statements = []
    for old_stmt in old_stmts:
        if old_stmt['id'] not in processed_old and (not old_stmt.get('match_id')):
            stmt = dict(old_stmt)
            stmt['change_status'] = stmt.get('change_status', 'deleted')
            if stmt['change_status'] in ('changed', 'moved'):
                # an old statement without a counterpart: the formatter would
                # otherwise print it as new code ("changed" without match = inserted)
                stmt['change_status'] = 'deleted'
            deleted_statements.append(stmt)
            processed_old.add(old_stmt['id'])

    # Group deleted statements by their control flow context
    control_flow_deleted = {}  # parent_control_flow_id -> [deleted_stmts]
    standalone_deleted = []

    for deleted_stmt in deleted_statements:
        parent_cf_id = find_control_flow_parent(deleted_stmt['id'], old_part_of_map, old_id_map, new_id_map)
        
        if parent_cf_id:
            if parent_cf_id not in control_flow_deleted:
                control_flow_deleted[parent_cf_id] = []
            control_flow_deleted[parent_cf_id].append(deleted_stmt)
        else:
            standalone_deleted.append(deleted_stmt)

    # Insert deleted statements that belong to control flow structures
    for parent_cf_id, cf_deleted_stmts in control_flow_deleted.items():
        # Find the corresponding control flow statement in merged
        parent_in_merged = None
        parent_idx = None
        
        for i, merged_stmt in enumerate(merged):
            # Check if this is the control flow statement or its match
            if (merged_stmt['id'] == parent_cf_id or 
                merged_stmt.get('match_id') == parent_cf_id or
                (merged_stmt.get('old_statement', {}).get('id') == parent_cf_id)):
                parent_in_merged = merged_stmt
                parent_idx = i
                break
        
        if parent_in_merged and parent_idx is not None:
            # Sort control flow deleted statements by their original order
            cf_deleted_with_order = []
            for deleted_stmt in cf_deleted_stmts:
                old_idx = old_order.index(deleted_stmt['id']) if deleted_stmt['id'] in old_order else 999999
                cf_deleted_with_order.append((old_idx, deleted_stmt))
            cf_deleted_with_order.sort(key=lambda x: x[0])
            
            # Group consecutive deleted statements by their part_of relationship and proximity
            grouped_deletions = group_consecutive_deleted_statements(
                cf_deleted_with_order, old_part_of_map, old_order)
            
            # Insert each group of deleted statements together
            for group in grouped_deletions:
                # Debug output for grouping
                if len(group) > 1:
                    group_ids = [stmt[1]['id'] for stmt in group]
                    #print(f"Inserting group of {len(group)} consecutive deleted statements: {group_ids}")
                
                # Try to insert into the control flow structure metadata for all statements in group
                for old_idx, deleted_stmt in group:
                    insert_deleted_statement_in_control_flow(
                        deleted_stmt, parent_in_merged, old_part_of_map)
                
                # Find the best position for the entire group
                first_stmt_id = group[0][1]['id']
                insert_pos = find_insertion_position_in_control_flow(
                    first_stmt_id, old_order, merged_ids, merged, 
                    parent_in_merged, parent_idx, old_part_of_map)
                
                # Insert all statements in the group at the same position (maintaining their relative order)
                for i, (old_idx, deleted_stmt) in enumerate(group):
                    merged.insert(insert_pos + i, deleted_stmt)
                    merged_ids.insert(insert_pos + i, deleted_stmt['id'])
                
                # Update parent_idx since we may have shifted positions
                if insert_pos <= parent_idx:
                    parent_idx += len(group)

    # Insert standalone deleted statements using position analysis
    # Sort standalone deleted statements by their original order in old_stmts
    standalone_deleted_with_order = []
    for deleted_stmt in standalone_deleted:
        old_idx = old_order.index(deleted_stmt['id']) if deleted_stmt['id'] in old_order else 999999
        standalone_deleted_with_order.append((old_idx, deleted_stmt))
    
    standalone_deleted_with_order.sort(key=lambda x: x[0])  # Sort by original order
    
    # Group consecutive standalone deleted statements
    standalone_groups = group_consecutive_standalone_statements(
        standalone_deleted_with_order, old_order)
    
    # Process each group of deleted statements together
    for group in standalone_groups:
        # Debug output for grouping
        if len(group) > 1:
            group_ids = [stmt[1]['id'] for stmt in group]
            #print(f"Inserting group of {len(group)} consecutive standalone deleted statements: {group_ids}")

        # Find insertion position for the first statement in the group
        first_stmt_id = group[0][1]['id']
        insert_pos = find_insertion_position(first_stmt_id, old_order, merged_ids, merged)

        # Insert all statements in the group at consecutive positions
        for i, (old_idx, deleted_stmt) in enumerate(group):
            merged.insert(insert_pos + i, deleted_stmt)
            merged_ids.insert(insert_pos + i, deleted_stmt['id'])

    # Step 4: Create ghost deleted entries for moved statements
    # For each moved statement, we create a "ghost deleted" copy that appears
    # at the OLD position (between its old neighbors). The moved statement
    # shows where it IS now (with + marker).
    #
    # Algorithm:
    # 1. Find the moved statement's position in old_order
    # 2. Find its NON-MOVED neighboring statements (skip over other moved statements)
    # 3. Check scope depth - if neighbor is a control flow block and moved stmt
    #    was at same scope, insert after the entire block, not inside
    # 4. Find where those neighbors ended up in merged (via match_id)
    # 5. Insert ghost between those neighbors in merged

    # Collect all moved old_ids for quick lookup
    moved_old_ids_set = set()
    for m_stmt in merged:
        if m_stmt.get('change_status') == 'moved':
            old_sub = m_stmt.get('old_statement', {})
            if old_sub and old_sub.get('id'):
                moved_old_ids_set.add(old_sub['id'])

    # Build a map from old_id to merged position (considering match_id)
    old_id_to_merged_idx = {}
    for i, m_stmt in enumerate(merged):
        if m_stmt.get('match_id'):
            old_id_to_merged_idx[m_stmt['match_id']] = i
        old_sub = m_stmt.get('old_statement', {})
        if old_sub and old_sub.get('id'):
            old_id_to_merged_idx[old_sub['id']] = i

    ghosts_to_insert = []  # List of (ghost_stmt, insert_position)

    for merged_stmt in merged:
        if merged_stmt.get('change_status') != 'moved':
            continue

        old_stmt = merged_stmt.get('old_statement', {})
        if not old_stmt:
            continue

        old_stmt_id = old_stmt.get('id')
        if not old_stmt_id or old_stmt_id not in old_order:
            continue

        old_stmt_scope = old_stmt.get('scope_level', 0)
        old_pos = old_order.index(old_stmt_id)

        # Find NON-MOVED previous neighbor at same or higher scope level
        prev_old_id = None
        for i in range(old_pos - 1, -1, -1):
            candidate_id = old_order[i]
            if candidate_id in moved_old_ids_set:
                continue  # Skip moved statements
            # Check scope level - only consider statements at same or lower depth
            candidate_stmt = old_id_map.get(candidate_id, {})
            candidate_scope = candidate_stmt.get('scope_level', 0)
            if candidate_scope <= old_stmt_scope:
                prev_old_id = candidate_id
                break

        # Find NON-MOVED next neighbor at same or higher scope level
        next_old_id = None
        for i in range(old_pos + 1, len(old_order)):
            candidate_id = old_order[i]
            if candidate_id in moved_old_ids_set:
                continue  # Skip moved statements
            candidate_stmt = old_id_map.get(candidate_id, {})
            candidate_scope = candidate_stmt.get('scope_level', 0)
            if candidate_scope <= old_stmt_scope:
                next_old_id = candidate_id
                break

        # Find where neighbors are in merged
        prev_merged_idx = old_id_to_merged_idx.get(prev_old_id) if prev_old_id else None
        next_merged_idx = old_id_to_merged_idx.get(next_old_id) if next_old_id else None

        # Determine insert position for ghost
        # When the previous neighbor is a control flow statement, prefer using next neighbor
        # because the merged list may have the control flow block containing moved statements
        # that weren't there in the old version.
        if prev_merged_idx is not None:
            prev_stmt = merged[prev_merged_idx]
            prev_type = prev_stmt.get('type', '')

            if prev_type in ['if_statement', 'switch_statement', 'for_statement',
                             'while_statement', 'do_statement', 'preproc_if']:
                # Previous neighbor is a control flow statement
                # Check if we have a valid next neighbor at the same scope level
                if next_merged_idx is not None:
                    # Prefer inserting before the next neighbor since the control flow
                    # block structure may have changed between old and new versions
                    insert_pos = next_merged_idx
                else:
                    # No next neighbor, find the end of the control flow block
                    block_end_idx = find_control_flow_block_end(prev_merged_idx, merged)
                    insert_pos = block_end_idx + 1
            else:
                # Insert after the previous neighbor
                insert_pos = prev_merged_idx + 1
        elif next_merged_idx is not None:
            # Insert before the next neighbor
            insert_pos = next_merged_idx
        else:
            # No valid neighbors found - try to insert at old position
            # relative to any non-moved statement
            insert_pos = len(merged)  # Default to end

        # Check if insert position would put the ghost at a deeper scope than its original scope
        # This can happen when statements moved INTO a control flow block - the ghost should
        # remain OUTSIDE the block at its original scope level
        if insert_pos < len(merged):
            target_scope = merged[insert_pos].get('scope_level', 0)
            if target_scope > old_stmt_scope:
                # The ghost would be inserted inside a deeper scope than where it originally was
                # Find the first statement at or below the ghost's original scope level
                # by scanning forward from insert_pos
                adjusted_pos = insert_pos
                for i in range(insert_pos, len(merged)):
                    stmt_at_i = merged[i]
                    if stmt_at_i.get('scope_level', 0) <= old_stmt_scope:
                        adjusted_pos = i
                        break
                else:
                    # No statement found at correct scope, append at end
                    adjusted_pos = len(merged)
                insert_pos = adjusted_pos

        # Create ghost deleted statement
        ghost_stmt = dict(old_stmt)
        ghost_stmt['id'] = f"ghost_{old_stmt_id}"
        ghost_stmt['change_status'] = 'moved_from'
        ghost_stmt['is_ghost_deleted'] = True
        # Remove match_id from ghost - the ghost represents the old position and
        # shouldn't be matched to the new statement's location in control flow blocks
        if 'match_id' in ghost_stmt:
            del ghost_stmt['match_id']

        ghosts_to_insert.append((ghost_stmt, insert_pos))

    # Sort by insert position (descending) so we insert from end to beginning
    # to avoid position shifts affecting subsequent insertions
    ghosts_to_insert.sort(key=lambda x: x[1], reverse=True)

    for ghost_stmt, insert_pos in ghosts_to_insert:
        merged.insert(insert_pos, ghost_stmt)
        merged_ids.insert(insert_pos, ghost_stmt['id'])

    # Also add ghost IDs to parent control flow statement_ids for proper rendering
    for ghost_stmt, _ in ghosts_to_insert:
        orig_old_id = ghost_stmt['id'].replace('ghost_', '')

        # Find which parent's part contained this statement in old code
        parent_info = find_parent_with_part_containing_stmt(orig_old_id, old_stmts)
        if not parent_info:
            continue

        old_parent_id, old_part = parent_info

        # Determine if this is a parts-based or additional_info-based parent
        is_additional_info = old_part.get('info') == 'contained_statements'

        # Find the merged version of this parent
        for m_stmt in merged:
            m_old = m_stmt.get('old_statement', {})
            is_match = (m_stmt.get('match_id') == old_parent_id or
                       m_old.get('id') == old_parent_id)
            if not is_match:
                continue

            # Found the parent - add ghost to appropriate location
            if is_additional_info:
                # Case statement: use additional_info.contained_statements
                for m_info in m_stmt.get('additional_info', []):
                    if m_info.get('info') == 'contained_statements':
                        stmt_ids = m_info.get('stmt_ids', [])
                        if ghost_stmt['id'] not in stmt_ids:
                            # Get old stmt_ids from old_part
                            old_stmt_ids = old_part.get('stmt_ids', [])
                            if orig_old_id in old_stmt_ids:
                                old_idx = old_stmt_ids.index(orig_old_id)
                                insert_at = 0
                                for prev_idx in range(old_idx - 1, -1, -1):
                                    prev_id = old_stmt_ids[prev_idx]
                                    if prev_id in moved_old_ids_set:
                                        continue
                                    # Find this in stmt_ids
                                    for check_idx, check_id in enumerate(stmt_ids):
                                        for m in merged:
                                            if m.get('id') == check_id:
                                                if (m.get('match_id') == prev_id or
                                                    m.get('old_statement', {}).get('id') == prev_id):
                                                    insert_at = check_idx + 1
                                                    break
                                        if insert_at > 0:
                                            break
                                    if insert_at > 0:
                                        break
                                stmt_ids.insert(insert_at, ghost_stmt['id'])
                        break
            else:
                # Standard parts-based control flow (if, for, while, etc.)
                for m_part in m_stmt.get('parts', []):
                    # Find corresponding part
                    if m_old:
                        for old_p in m_old.get('parts', []):
                            if old_p.get('id') == old_part.get('id'):
                                stmt_ids = m_part.get('statement_ids', [])
                                if ghost_stmt['id'] not in stmt_ids:
                                    # Insert ghost after its prev non-moved neighbor
                                    old_stmt_ids = old_part.get('statement_ids', [])
                                    if orig_old_id in old_stmt_ids:
                                        old_idx = old_stmt_ids.index(orig_old_id)
                                        insert_at = 0
                                        for prev_idx in range(old_idx - 1, -1, -1):
                                            prev_id = old_stmt_ids[prev_idx]
                                            if prev_id in moved_old_ids_set:
                                                continue
                                            # Find this in stmt_ids
                                            for check_idx, check_id in enumerate(stmt_ids):
                                                for m in merged:
                                                    if m.get('id') == check_id:
                                                        if (m.get('match_id') == prev_id or
                                                            m.get('old_statement', {}).get('id') == prev_id):
                                                            insert_at = check_idx + 1
                                                            break
                                                if insert_at > 0:
                                                    break
                                            if insert_at > 0:
                                                break
                                        stmt_ids.insert(insert_at, ghost_stmt['id'])
                                break
            break

    # Create variable mapping based on the merge process
    var_mapping = create_variable_mapping_during_merge(old_stmts, new_stmts, match_pairs)

    return merged, var_mapping

def group_consecutive_deleted_statements(cf_deleted_with_order: List[Tuple[int, Dict[str, Any]]], 
                                        part_of_map: Dict[str, str], 
                                        old_order: List[str]) -> List[List[Tuple[int, Dict[str, Any]]]]:
    """
    Group consecutive deleted statements that belong to the same control flow part.
    This preserves the relative order of statements that were originally adjacent.
    
    Returns a list of groups, where each group is a list of (old_idx, deleted_stmt) tuples.
    """
    if not cf_deleted_with_order:
        return []
    
    groups = []
    current_group = [cf_deleted_with_order[0]]
    
    for i in range(1, len(cf_deleted_with_order)):
        prev_old_idx, prev_stmt = cf_deleted_with_order[i-1]
        curr_old_idx, curr_stmt = cf_deleted_with_order[i]
        
        # Get the part_of information for both statements
        prev_part_of = part_of_map.get(prev_stmt['id'])
        curr_part_of = part_of_map.get(curr_stmt['id'])
        
        # Check if statements are consecutive and belong to the same part
        are_consecutive = (curr_old_idx - prev_old_idx <= 2)  # Allow for small gaps
        same_part = (prev_part_of == curr_part_of and prev_part_of is not None)
        
        # Also check if they are actually consecutive in the original order
        # (allowing for one statement in between that might not be deleted)
        consecutive_in_original = False
        if prev_old_idx + 1 < len(old_order) and curr_old_idx < len(old_order):
            gap_size = curr_old_idx - prev_old_idx
            if gap_size <= 2:  # Direct neighbors or one statement apart
                consecutive_in_original = True
        
        if are_consecutive and same_part and consecutive_in_original:
            # Add to current group
            current_group.append(cf_deleted_with_order[i])
        else:
            # Start a new group
            groups.append(current_group)
            current_group = [cf_deleted_with_order[i]]
    
    # Don't forget the last group
    groups.append(current_group)
    
    return groups

def group_consecutive_standalone_statements(standalone_deleted_with_order: List[Tuple[int, Dict[str, Any]]], 
                                          old_order: List[str]) -> List[List[Tuple[int, Dict[str, Any]]]]:
    """
    Group consecutive standalone deleted statements to preserve their relative order.
    
    Returns a list of groups, where each group is a list of (old_idx, deleted_stmt) tuples.
    """
    if not standalone_deleted_with_order:
        return []
    
    groups = []
    current_group = [standalone_deleted_with_order[0]]
    
    for i in range(1, len(standalone_deleted_with_order)):
        prev_old_idx, prev_stmt = standalone_deleted_with_order[i-1]
        curr_old_idx, curr_stmt = standalone_deleted_with_order[i]
        
        # Check if statements are consecutive in the original order
        # Allow for small gaps (1-2 statements) that might be matched/inserted statements
        gap_size = curr_old_idx - prev_old_idx
        are_consecutive = gap_size <= 3  # Allow up to 2 statements in between
        
        if are_consecutive:
            # Add to current group
            current_group.append(standalone_deleted_with_order[i])
        else:
            # Start a new group
            groups.append(current_group)
            current_group = [standalone_deleted_with_order[i]]
    
    # Don't forget the last group
    groups.append(current_group)
    
    return groups

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Merge two statement lists with intelligent ordering.')
    parser.add_argument('--old', required=True, help='Path to old statements JSON')
    parser.add_argument('--new', required=True, help='Path to new statements JSON')
    parser.add_argument('--out', required=True, help='Path to output merged JSON')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    old_stmts = load_statements(args.old)
    new_stmts = load_statements(args.new)
    merged, var_mapping = merge_statements(old_stmts, new_stmts)

    with open(args.out, 'w') as f:
        json.dump(merged, f, indent=2)
    
    # Save variable mapping to a separate file
    mapping_file = args.out.replace('.json', '_variable_mapping.json')
    with open(mapping_file, 'w') as f:
        json.dump(var_mapping, f, indent=2)
    
    if args.debug:
        print(f"Debug: Merged {len(old_stmts)} old and {len(new_stmts)} new statements")
        print(f"Result: {len(merged)} merged statements")
        print(f"Variable mapping: {len(var_mapping)} mappings created")
        
        # Show deleted statements and their positions
        deleted_stmts = [s for s in merged if s.get('change_status') == 'deleted']
        print(f"Deleted statements: {len(deleted_stmts)}")
        for i, stmt in enumerate(merged):
            if stmt.get('change_status') == 'deleted':
                expr = stmt.get('expression', 'N/A')[:30]
                print(f"  Position {i}: {expr}")
    
    print(f"Merged {len(old_stmts)} old and {len(new_stmts)} new statements into {len(merged)} merged statements.")
    print(f"Output: {args.out}")
    print(f"Variable mapping: {mapping_file}")

if __name__ == '__main__':
    main()
