"""
Function to create the matching between the AST nodes of the two versions of the code.
"""
import bisect
import os

from collections import defaultdict

CHANGE_PRIORITY = {
    "changed": 5,
    "deleted": 4,
    "inserted": 3,
    "moved": 2,
    "matched": 1
}

def lookup_line_info(line_lookup, line_number):
    """
    Retrieves the initial line information and file details for a given line number.

    :param line_lookup: The pre-built lookup dictionary.
    :param line_number: The line number to look up.
    :return: A dictionary containing file info, function name, and initial lines or None if not found.
    """
    if not isinstance(line_lookup, dict):
        return None
    return line_lookup.get(line_number, None)

def get_relative_path(file_path, root_dir):
    """
    Get the relative path of a file from a root directory
    """
    return os.path.relpath(file_path, root_dir)

def extract_function_params(calls_info):
    """Extract {function_name: [param_names]} from calls_info."""
    func_map = {}
    for call in calls_info:
        func_name = call["function_name"]
        params = [arg["name"] for arg in call["arguments"]]
        func_map[func_name] = params
    return func_map

def find_first_matching_tuple(ast_mapping, relative_key, line_number):
    """
    Finds the first tuple (start_line, end_line, ast_file) where:
    start_line <= line_number <= end_line.

    :param ast_mapping: Dictionary mapping relative_key -> list of (start, end, file).
    :param relative_key: The relative key to look up.
    :param line_number: The target line number.
    :return: The first matching tuple or None if no match is found.
    """
    if relative_key not in ast_mapping:
        return None  # Key not found

    for start_line, end_line, ast_file in ast_mapping[relative_key]:
        if start_line is None or end_line is None or ast_file is None:
            continue
        if start_line <= line_number <= end_line:
            return (start_line, end_line, ast_file)  # Return first match

    return None  # No match found

def find_most_specific_stmt(sorted_stmts, start, end):
    # Build keys using the same sorting logic: start as is, and negative of end components.
    sorted_keys = [(stmt.start, -stmt.end[0], -stmt.end[1]) for stmt in sorted_stmts]
    lookup_key = (start, -end[0], -end[1])
    
    # Find insertion point. Note that bisect_right returns an index where our lookup_key would go.
    index = bisect.bisect_right(sorted_keys, lookup_key) - 1
    best_match = None
    
    # Walk backwards from that index until you find a statement that contains the source range.
    for i in range(index, -1, -1):
        stmt = sorted_stmts[i]
        if stmt.contains(start, end):
            best_match = stmt
            break  # Because of our sorting, the first valid candidate is the most specific.

    # if best_match is None: find the best match where the start line is the same
    if best_match is None:
        for stmt in sorted_stmts:
            if stmt.start[0] == start[0]:
                best_match = stmt
                break

    # if best_match is None: find the best match where the end line is the same
    if best_match is None:
        for stmt in sorted_stmts:
            if stmt.end[0] == end[0]:
                best_match = stmt
                break
    
    return best_match.id if best_match else None

def find_most_specific_stmts(valid_stmts, start, end):
    """
    Find the most specific statement that contains the given range.
    
    If a single specific statement can't be found, try to find multiple
    statements that collectively cover the range before falling back to
    control flow nodes with ignore flag.
    """
    # Check for exact match in valid statements
    exact_matches = [stmt for stmt in valid_stmts if stmt.start == start and stmt.end == end]
    if exact_matches:
        return [exact_matches[0].id]
    
    # Check for containing statements in valid statements
    containing_stmts = [stmt for stmt in valid_stmts if stmt.contains(start, end)]
    if containing_stmts:
        # Sort by size (smaller scope first)
        containing_stmts.sort(key=lambda s: (s.end[0] - s.start[0], s.end[1] - s.start[1]))
        return [containing_stmts[0].id]
    
    # Multi-line or multi-statement handling
    # Find all statements that overlap with any part of the range
    overlapping_stmts = []
    
    for stmt in valid_stmts:
        # A statement overlaps if:
        # 1. It starts before or at the end position AND
        # 2. It ends after or at the start position
        if ((stmt.start[0] < end[0] or (stmt.start[0] == end[0] and stmt.start[1] <= end[1])) and 
            (stmt.end[0] > start[0] or (stmt.end[0] == start[0] and stmt.end[1] >= start[1]))):
            overlapping_stmts.append(stmt)
    
    if overlapping_stmts:
        # For your specific example where we need statements covering different lines
        # First, organize statements by the lines they cover
        line_coverage = {}
        for line in range(start[0], end[0] + 1):
            line_coverage[line] = []
            
        for stmt in overlapping_stmts:
            # Add this statement to all lines it covers
            for line in range(max(stmt.start[0], start[0]), min(stmt.end[0], end[0]) + 1):
                line_coverage[line].append(stmt)

        if start[0] == end[0]:  # Single-line change
            # For single line, ensure statements cover the column range
            for line, stmts in line_coverage.items():
                filtered_stmts = []
                for stmt in stmts:
                    # Check if statement covers the target column range
                    if (stmt.start[0] == start[0] and stmt.end[0] == end[0] and
                        stmt.start[1] <= start[1] and stmt.end[1] >= end[1]):
                        filtered_stmts.append(stmt)
                line_coverage[line] = filtered_stmts

        selected_stmts = set()
        for line, stmts in line_coverage.items():
            if not stmts:
                continue
                
            # For each line, find the most appropriate statement based on line position
            if line == start[0]:  # First line of the range
                # For the first line, select the statement that covers the most area from the start column
                # No filtering based on start column
                if stmts:
                    # Sort by end position (prefer statements that extend furthest right)
                    line_stmts = sorted(stmts, key=lambda s: float('inf') if s.end[0] > line else s.end[1], reverse=True)
                    # Choose statement that covers the most area (highest priority to multi-line statements)
                    best_stmt = max(stmts, key=lambda s: (
                        2 if s.start[1] <= start[1] else 1,  # Priority to statements that start before target
                        float('inf') if s.end[0] > line else s.end[1]  # Then by how far they extend
                    ))
                    selected_stmts.add(best_stmt)
                    
            elif line == end[0]:  # Last line of the range
                # For the last line, select the statement that covers the most area up to the end column
                # No filtering based on end column
                if stmts:
                    # Choose statement that covers the most area (highest priority to multi-line statements)
                    best_stmt = max(stmts, key=lambda s: (
                        2 if s.end[1] >= end[1] else 1,  # Priority to statements that end after target
                        -s.start[1] if s.start[0] == line else float('inf')  # Then by how early they start
                    ))
                    selected_stmts.add(best_stmt)
                    
            else:  # Middle lines of the range
                # For middle lines, find statements that cover as much of the line as possible
                if stmts:
                    # Sort by coverage within this line (prefer statements that cover the entire line)
                    multi_line_stmts = [s for s in stmts if s.start[0] < line and s.end[0] > line]
                    if multi_line_stmts:
                        # A multi-line statement that fully contains this line is ideal
                        selected_stmts.add(multi_line_stmts[0])
                    else:
                        # Otherwise, find statements that start earliest and end latest on this line
                        if stmts:
                            earliest_start = min(stmts, key=lambda s: s.start[1] if s.start[0] == line else float('inf'))
                            latest_end = max(stmts, key=lambda s: s.end[1] if s.end[0] == line else 0)
                            
                            if earliest_start == latest_end:
                                selected_stmts.add(earliest_start)
                            else:
                                selected_stmts.add(earliest_start)
                                selected_stmts.add(latest_end)
        
        
        # Check if we have coverage for all lines
        # if selected_stmts and all(line_coverage[line] for line in line_coverage):
        #     return [stmt.id for stmt in selected_stmts]
        
        # Return selected statements if we have any, even if not all lines have coverage
        if selected_stmts:
            # Check how much of the range we're covering
            covered_lines = sum(1 for line in line_coverage if line_coverage[line])
            total_lines = end[0] - start[0] + 1
            
            # If we cover at least half the lines or have statements for both start and end lines,
            # return the selected statements
            if (covered_lines >= total_lines / 2 or 
                (start[0] in line_coverage and line_coverage[start[0]] and 
                 end[0] in line_coverage and line_coverage[end[0]])):
                # in source order: a set of Statement objects iterates by address
                return [stmt.id for stmt in sorted(selected_stmts, key=lambda s: (s.start, s.end))]
    
    # Fall back to statements with matching start or end line
    for stmt in valid_stmts:
        if stmt.start[0] == start[0]:
            return [stmt.id]
    
    for stmt in valid_stmts:
        if stmt.end[0] == end[0]:
            return [stmt.id]
    
    return []

def find_stmt_change_status(json_data, stmt_id):
    """
    Retrieves the current change_status of a statement from the JSON data.
    
    :param json_data: The JSON representation of the AST file.
    :param stmt_id: The statement ID to look up.
    :return: The change_status if found, else None.
    """
    for stmt in json_data:
        if stmt["id"] == stmt_id:
            return stmt.get("change_status"), stmt.get("match_id", None)
    return None, None

def get_higher_priority_status(existing_status, new_status):
    """
    Determines the higher priority change_status.
    If existing_status has lower priority, it's replaced by new_status.
    
    :param existing_status: The current status of the statement.
    :param new_status: The new status that might replace it.
    :return: The higher priority status.
    """
    existing_priority = CHANGE_PRIORITY.get(existing_status, 0)
    new_priority = CHANGE_PRIORITY.get(new_status, 0)

    return new_status if new_priority >= existing_priority else existing_status

def find_stmt_and_modify(json_data, statement_id, new_data):
    """
    Find a statement by its ID and modify its data.
    """
    for stmt in json_data["statements"]:
        if stmt.get("id") == statement_id:
            stmt.update(new_data)
            return True
    return False

def _le_pos(a, b):
    """
    Return True if position a <= b lexicographically:
      line_a < line_b  or  (line_a == line_b  and  col_a <= col_b)
    """
    return (a[0] < b[0]) or (a[0] == b[0] and a[1] <= b[1])

class Statement:
    def __init__(self, data):
        self.id = data["id"]
        self.start = (int(data["start"][0]), int(data["start"][1]))
        self.end = (int(data["end"][0]), int(data["end"][1]))

    def contains(self, start, end):
        """
        True if [start,end] lies entirely within [self.start,self.end], i.e.
          self.start <= start  and  end <= self.end
        """
        return _le_pos(self.start, start) and _le_pos(end, self.end)
        # return self.start <= start and self.end >= end
    
    def __repr__(self):
        return f"Statement(id={self.id}, start={self.start}, end={self.end})"
    
def load_statements(json_data):
    """Load statements from JSON into Statement objects."""
    statements = [Statement(entry) for entry in json_data if not any(
        isinstance(info, dict) and info.get("ignore") == True
        for info in entry.get("additional_info", [])
    )]
    # statements = [Statement(entry) for entry in json_data]
    statements.sort(key=lambda s: (s.start[0], s.start[1], -s.end[0], -s.end[1]))
    return statements

class NodeMatcher:
    def __init__(self, matches_mapping, changes_mapping, old_line_lookup, new_line_lookup, old_ast_mapping, new_ast_mapping, root_dir_old, root_dir_new, ast_json_objs):
        """
        matches_mapping from gumtree char representation: [Dict]
            Each Dict contains: src_start, src_end, dst_start, dst_end
            0-based lines and columns
        """
        self.matches_mapping = matches_mapping

        """
        changes mapping from gumtree char representation: [Dict]
            Each Dict contains: action, start_line(_old/_new), end_line(_old/_new), start_col(_old/_new), end_col(_old/_new)
            0-based lines and columns
        """
        self.changes_mapping = changes_mapping
        #print(f"changes_mapping: {json.dumps(self.changes_mapping, indent=4)}")

        """
        old_line_lookup: Dict{Dict}
            key: line number of the shortened file
            value: Dict{
                "initial_line": line_number in the original file
                "file": file path to the original file,
                "type": old/new
                "function": function name
            }
        """
        self.old_line_lookup = old_line_lookup

        """
        mew_line_lookup: Dict{Dict} --> same as old_line_lookup
        """
        self.new_line_lookup = new_line_lookup

        """
        old_ast_mapping: Dict{Dict}
            key: file path
            value: [
                (start_line, end_line, key in the ast_json_objs to access the ast statements (e.g. outputs/new_version/src/h2_67f350_54_63))
            ]
        for each value in the old mapping, there is value in the new mapping (same order)
        """
        self.old_ast_mapping = old_ast_mapping
        # print(f"old_ast_mapping: {json.dumps(self.old_ast_mapping, indent=4)}")

        """
        new_ast_mapping: Dict{Dict} --> same as old_ast_mapping
        """
        self.new_ast_mapping = new_ast_mapping

        """
        root_dir_old: str
            root directory of the old version of the code
        """
        self.root_dir_old = root_dir_old

        """
        root_dir_new: str --> same as root_dir_old
        """
        self.root_dir_new = root_dir_new

        """
        ast_json_objs: List{Dict}
            List of dictionaries containing the ast statements for each entry in the ast_mapping
        """
        self.ast_json_objs = ast_json_objs
        #logging.info(json.dumps(self.ast_json_objs, indent=4))
        # print(ast_json_objs)

        self.statement_store = defaultdict(list)

        # (old statement id, new statement id) -> how directly a GumTree match
        # ties the two (see _note_match_evidence); both key orders are stored
        self.pair_evidence = {}
        self._stmt_index = {}


    def matching_stmts(self, g_ctx=False, file_arr=None):
        """
        Create a mapping between the AST nodes of the two versions of the code.

        Args:
            g_ctx: If True, indicates global context matching (uses file_arr directly)
            file_arr: For global context, a list of [old_ast_file, new_ast_file] to use directly

        Returns:
            Dictionary mapping source AST file -> list of statement match records
        """
        statement_mapping = {}

        for match in self.matches_mapping:
            # s = start, e = end, l = line, c = column
            src_s_l, src_s_c = match["src_start"]
            src_e_l, src_e_c = match["src_end"]
            dst_s_l, dst_s_c = match["dst_start"]
            dst_e_l, dst_e_c = match["dst_end"]

            # Only consider lines inside interesting functions/context
            if src_s_l not in self.old_line_lookup or src_e_l not in self.old_line_lookup:
                continue
            if dst_s_l not in self.new_line_lookup or dst_e_l not in self.new_line_lookup:
                continue

            src_s_info = lookup_line_info(self.old_line_lookup, src_s_l)
            src_e_info = lookup_line_info(self.old_line_lookup, src_e_l)
            dst_s_info = lookup_line_info(self.new_line_lookup, dst_s_l)
            dst_e_info = lookup_line_info(self.new_line_lookup, dst_e_l)

            # Skip if any info is None (shouldn't happen after lookup check, but be safe)
            if not all([src_s_info, src_e_info, dst_s_info, dst_e_info]):
                continue

            src_rel_path = get_relative_path(f"/{src_s_info['file']}", self.root_dir_old)
            dst_rel_path = get_relative_path(f"/{dst_s_info['file']}", self.root_dir_new)

            # Get AST tuples - either from mapping or directly from file_arr for global context
            src_ast_tuple = find_first_matching_tuple(self.old_ast_mapping, src_rel_path, src_s_info["initial_line"])
            dst_ast_tuple = find_first_matching_tuple(self.new_ast_mapping, dst_rel_path, dst_s_info["initial_line"])

            # If not found and we have file_arr (global context), use it directly
            if src_ast_tuple is None and g_ctx and file_arr and len(file_arr) >= 1:
                # For global context, create a synthetic tuple that spans all lines
                old_max_line = max(self.old_line_lookup.keys()) if self.old_line_lookup else 0
                src_ast_tuple = (0, old_max_line, file_arr[0])

            if dst_ast_tuple is None and g_ctx and file_arr and len(file_arr) >= 2:
                new_max_line = max(self.new_line_lookup.keys()) if self.new_line_lookup else 0
                dst_ast_tuple = (0, new_max_line, file_arr[1])

            # Skip if we still can't find the AST tuple
            if src_ast_tuple is None:
                print(f"Warning: No AST mapping found for source file {src_rel_path} at line {src_s_info['initial_line']} for match: {match}")
                continue

            if dst_ast_tuple is None:
                print(f"Warning: No AST mapping found for dest file {dst_rel_path} at line {dst_s_info['initial_line']} for match: {match}")
                continue

            # Get the AST file key from the tuple
            src_ast_file = src_ast_tuple[2]
            dst_ast_file = dst_ast_tuple[2]

            # Skip if AST file keys are None
            if src_ast_file is None or dst_ast_file is None:
                continue

            # Load or retrieve statements for source file
            if src_ast_file not in self.statement_store:
                src_code = self.ast_json_objs.get(src_ast_file)
                if src_code is None:
                    print(f"Warning: AST object not found for source file {src_ast_file}")
                    continue
                src_stmts = load_statements(src_code.get("statements", []))
                self.statement_store[src_ast_file] = src_stmts
            else:
                src_stmts = self.statement_store[src_ast_file]

            # Load or retrieve statements for destination file
            if dst_ast_file not in self.statement_store:
                dst_code = self.ast_json_objs.get(dst_ast_file)
                if dst_code is None:
                    print(f"Warning: AST object not found for dest file {dst_ast_file}")
                    continue
                dst_stmts = load_statements(dst_code.get("statements", []))
                self.statement_store[dst_ast_file] = dst_stmts
            else:
                dst_stmts = self.statement_store[dst_ast_file]

            # Find matching statements
            src_stmt_ids = find_most_specific_stmts(src_stmts, (src_s_info["initial_line"], src_s_c), (src_e_info["initial_line"], src_e_c))
            dst_stmt_ids = find_most_specific_stmts(dst_stmts, (dst_s_info["initial_line"], dst_s_c), (dst_e_info["initial_line"], dst_e_c))

            # Skip if no statements found
            if not src_stmt_ids or not dst_stmt_ids:
                continue

            self._note_match_evidence(
                src_ast_file, src_stmt_ids, (src_s_info["initial_line"], src_s_c), (src_e_info["initial_line"], src_e_c),
                dst_ast_file, dst_stmt_ids, (dst_s_info["initial_line"], dst_s_c), (dst_e_info["initial_line"], dst_e_c))

            if src_ast_file not in statement_mapping:
                statement_mapping[src_ast_file] = []

            # IMPROVED MATCHING LOGIC
            if len(src_stmt_ids) == 1 and len(dst_stmt_ids) == 1:
                # if the statements are of a different type, we cannot match them
                src_stmts_for_type = self.ast_json_objs[src_ast_file].get("statements", [])
                dst_stmts_for_type = self.ast_json_objs[dst_ast_file].get("statements", [])
                src_stmt_type = next((s["type"] for s in src_stmts_for_type if s["id"] == src_stmt_ids[0]), None)
                dst_stmt_type = next((s["type"] for s in dst_stmts_for_type if s["id"] == dst_stmt_ids[0]), None)

                if src_stmt_type != dst_stmt_type:
                    continue

                # Simple one-to-one case
                statement_mapping[src_ast_file].append({
                    "src_file": src_ast_file,
                    "dst_file": dst_ast_file,
                    "src_stmt": src_stmt_ids[0],
                    "dst_stmt": dst_stmt_ids[0],
                    "src_update": {"match_id": dst_stmt_ids[0], "change_status": "matched"},
                    "dst_update": {"match_id": src_stmt_ids[0], "change_status": "matched"}
                })
            else:
                # Multiple statements case - need smarter matching
                # Get actual statement objects for comparison
                src_stmt_objs = []
                for stmt_id in src_stmt_ids:
                    for s in self.ast_json_objs[src_ast_file].get("statements", []):
                        if s["id"] == stmt_id:
                            src_stmt_objs.append(s)
                            break

                dst_stmt_objs = []
                for stmt_id in dst_stmt_ids:
                    for s in self.ast_json_objs[dst_ast_file].get("statements", []):
                        if s["id"] == stmt_id:
                            dst_stmt_objs.append(s)
                            break

                # Match statements by type and name
                for src_stmt in src_stmt_objs:
                    matched = False
                    for dst_stmt in dst_stmt_objs:
                        # Skip already matched destination statements
                        if any(entry.get("dst_stmt") == dst_stmt["id"] for entry in statement_mapping.get(src_ast_file, [])):
                            continue

                        # Check if statements are compatible
                        if self._are_statements_compatible(src_stmt, dst_stmt):
                            statement_mapping[src_ast_file].append({
                                "src_file": src_ast_file,
                                "dst_file": dst_ast_file,
                                "src_stmt": src_stmt["id"],
                                "dst_stmt": dst_stmt["id"],
                                "src_update": {"match_id": dst_stmt["id"], "change_status": "matched"},
                                "dst_update": {"match_id": src_stmt["id"], "change_status": "matched"}
                            })
                            matched = True
                            break
                
        # logging.info(json.dumps(statement_mapping, indent=4))

        return statement_mapping
    
    def _stmt_by_id(self, ast_file):
        index = self._stmt_index.get(ast_file)
        if index is None:
            index = {s.id: s for s in self.statement_store.get(ast_file, [])}
            if index:  # cache once the file's statements are loaded
                self._stmt_index[ast_file] = index
        return index

    def _note_match_evidence(self, src_file, src_ids, src_start, src_end, dst_file, dst_ids, dst_start, dst_end):
        """
        Remember how directly a GumTree match ties each (old, new) statement pair:
        2 if the matched nodes are the two statements themselves, 1 if one side
        is, 0 if the match lies inside both. When several old statements claim
        the same new one (or vice versa), _postprocess_matches keeps the pair
        with the strongest evidence: the statement GumTree mapped as a whole
        beats a statement that merely contains a matched sub-expression.
        """
        src_index = self._stmt_by_id(src_file)
        dst_index = self._stmt_by_id(dst_file)

        def exact(index, sid, start, end):
            stmt = index.get(sid)
            return stmt is not None and stmt.start == tuple(start) and stmt.end == tuple(end)

        for sid in src_ids:
            src_exact = exact(src_index, sid, src_start, src_end)
            for did in dst_ids:
                score = int(src_exact) + int(exact(dst_index, did, dst_start, dst_end))
                if score > self.pair_evidence.get((sid, did), -1):
                    self.pair_evidence[(sid, did)] = score
                    self.pair_evidence[(did, sid)] = score

    def _are_statements_compatible(self, src_stmt, dst_stmt):
        """
        Determine if two statements are compatible for matching.
        """
        # If types don't match, generally they're not compatible
        if src_stmt["type"] != dst_stmt["type"]:
                return False
        
        # For variable declarations, check for same variable names
        if src_stmt["type"] == "declaration":
            src_vars = {var["name"] for var in src_stmt.get("left_side", []) if var.get("id_type", "variable") == "variable"}
            dst_vars = {var["name"] for var in dst_stmt.get("left_side", []) if var.get("id_type", "variable") == "variable"}
            
            # If they declare the same variable, they're likely a match
            return bool(src_vars.intersection(dst_vars))
        
        # For assignments, check the left side variable
        elif src_stmt["type"] == "expression_statement":
            src_left = {var["name"] for var in src_stmt.get("left_side", []) if var.get("id_type", "variable") == "variable"}
            dst_left = {var["name"] for var in dst_stmt.get("left_side", []) if var.get("id_type", "variable") == "variable"}
            
            # If they modify the same variable, they're likely a match
            return bool(src_left.intersection(dst_left))
        
        # For function calls, check the function name
        elif src_stmt["calls_info"] is not None and len(src_stmt["calls_info"]) > 0 and dst_stmt["calls_info"] is not None and len(dst_stmt["calls_info"]) > 0:
            src_stmt_calls = extract_function_params(src_stmt["calls_info"])
            dst_stmt_calls = extract_function_params(dst_stmt["calls_info"])

            for func in src_stmt_calls:
                if func in dst_stmt_calls and src_stmt_calls[func] == dst_stmt_calls[func]:
                    # If they call the same function with the same parameters, they're likely a match
                    return True
            # If no matching function calls found, they're not compatible
            return False
        
        # For other types, check if expressions are similar
        elif "expression" in src_stmt and "expression" in dst_stmt:
            return src_stmt["expression"] == dst_stmt["expression"]
        
        # Default case
        return False

    def matching_changes(self, g_ctx=False, file_arr=None, match_mapping=None):
        """
        Create a mapping between the changes in the two versions of the code.

        Args:
            g_ctx: If True, indicates global context matching (uses file_arr directly)
            file_arr: For global context, a list of [old_ast_file, new_ast_file] to use directly
            match_mapping: the statement matches (from matching_stmts); an update
                action names the OLD node, so its counterpart in the new version
                is found through the match and marked changed as well

        Returns:
            Dictionary mapping AST file -> list of change records
        """
        change_mapping = {}
        counterpart = {}  # old statement id -> (new ast file, new statement id)
        for records in (match_mapping or {}).values():
            for r in records:
                if r.get("src_stmt") and r.get("dst_stmt"):
                    counterpart[r["src_stmt"]] = (r.get("dst_file"), r["dst_stmt"])

        for change in self.changes_mapping:
            action = change["action"]

            # Get line info based on action type
            if action == "move-tree":
                src_s_info = lookup_line_info(self.old_line_lookup, change.get("start_line_old"))
                src_e_info = lookup_line_info(self.old_line_lookup, change.get("end_line_old"))
                dst_s_info = lookup_line_info(self.new_line_lookup, change.get("start_line_new"))
                dst_e_info = lookup_line_info(self.new_line_lookup, change.get("end_line_new"))
            else:
                src_s_info = lookup_line_info(self.old_line_lookup, change.get("start_line"))
                src_e_info = lookup_line_info(self.old_line_lookup, change.get("end_line"))
                dst_s_info = lookup_line_info(self.new_line_lookup, change.get("start_line"))
                dst_e_info = lookup_line_info(self.new_line_lookup, change.get("end_line"))

            # Handle insert actions (target is new/destination file)
            if action in ("insert-tree", "insert-node"):
                # Skip if both dst infos are None (e.g., comment inserted)
                if dst_s_info is None and dst_e_info is None:
                    continue

                # Need at least dst_s_info to proceed
                if dst_s_info is None:
                    continue

                dst_rel_path = get_relative_path(f"/{dst_s_info['file']}", self.root_dir_new)
                dst_ast_tuple = find_first_matching_tuple(self.new_ast_mapping, dst_rel_path, dst_s_info["initial_line"])

                # Fallback to file_arr for global context
                if dst_ast_tuple is None and g_ctx and file_arr and len(file_arr) >= 2:
                    new_max_line = max(self.new_line_lookup.keys()) if self.new_line_lookup else 0
                    dst_ast_tuple = (0, new_max_line, file_arr[1])

                if dst_ast_tuple is None:
                    print(f"Warning: No AST mapping found for destination file {dst_rel_path} at line {dst_s_info['initial_line']} for change: {change}")
                    continue

                dst_ast_file = dst_ast_tuple[2]
                if dst_ast_file is None:
                    continue

                # Load statements
                if dst_ast_file not in self.statement_store:
                    dst_code = self.ast_json_objs.get(dst_ast_file)
                    if dst_code is None:
                        print(f"Warning: AST object not found for dest file {dst_ast_file}")
                        continue
                    dst_stmts = load_statements(dst_code.get("statements", []))
                    self.statement_store[dst_ast_file] = dst_stmts
                else:
                    dst_stmts = self.statement_store[dst_ast_file]

                # Find matching statements
                end_line = dst_e_info["initial_line"] if dst_e_info else dst_s_info["initial_line"]
                dst_stmt_ids = find_most_specific_stmts(
                    dst_stmts,
                    (dst_s_info["initial_line"], change.get("start_col", 0)),
                    (end_line, change.get("end_col", 0))
                )

                if not dst_stmt_ids:
                    continue

                if dst_ast_file not in change_mapping:
                    change_mapping[dst_ast_file] = []

                for dst_stmt_id in dst_stmt_ids:
                    change_mapping[dst_ast_file].append({
                        "src_file": None,
                        "dst_file": dst_ast_file,
                        "src_stmt": None,
                        "dst_stmt": dst_stmt_id,
                        "src_update": {},
                        "dst_update": {"change_status": "inserted"}
                    })

            # Handle delete and update actions: GumTree positions them in the
            # OLD file (an update names the old node and its new label)
            elif action in ("delete-tree", "delete-node", "update-tree", "update-node"):
                # Need src_s_info to proceed
                if src_s_info is None:
                    continue

                src_rel_path = get_relative_path(f"/{src_s_info['file']}", self.root_dir_old)
                src_ast_tuple = find_first_matching_tuple(self.old_ast_mapping, src_rel_path, src_s_info["initial_line"])

                # Fallback to file_arr for global context
                if src_ast_tuple is None and g_ctx and file_arr and len(file_arr) >= 1:
                    old_max_line = max(self.old_line_lookup.keys()) if self.old_line_lookup else 0
                    src_ast_tuple = (0, old_max_line, file_arr[0])

                if src_ast_tuple is None:
                    print(f"Warning: No AST mapping found for source file {src_rel_path} at line {src_s_info['initial_line']} for change: {change}")
                    continue

                src_ast_file = src_ast_tuple[2]
                if src_ast_file is None:
                    continue

                # Load statements
                if src_ast_file not in self.statement_store:
                    src_code = self.ast_json_objs.get(src_ast_file)
                    if src_code is None:
                        print(f"Warning: AST object not found for source file {src_ast_file}")
                        continue
                    src_stmts = load_statements(src_code.get("statements", []))
                    self.statement_store[src_ast_file] = src_stmts
                else:
                    src_stmts = self.statement_store[src_ast_file]

                # Find matching statements
                end_line = src_e_info["initial_line"] if src_e_info else src_s_info["initial_line"]

                # For delete-tree, try with col-1 first (account for missing semicolon)
                if action == "delete-tree":
                    src_stmt_ids = find_most_specific_stmts(
                        src_stmts,
                        (src_s_info["initial_line"], change.get("start_col", 0)),
                        (end_line, change.get("end_col", 1) - 1)
                    )
                    if not src_stmt_ids:
                        src_stmt_ids = find_most_specific_stmts(
                            src_stmts,
                            (src_s_info["initial_line"], change.get("start_col", 0)),
                            (end_line, change.get("end_col", 0))
                        )
                else:
                    src_stmt_ids = find_most_specific_stmts(
                        src_stmts,
                        (src_s_info["initial_line"], change.get("start_col", 0)),
                        (end_line, change.get("end_col", 0))
                    )

                if not src_stmt_ids:
                    continue

                if src_ast_file not in change_mapping:
                    change_mapping[src_ast_file] = []

                change_status = "deleted" if action == "delete-tree" else "changed"
                for src_stmt_id in src_stmt_ids:
                    change_mapping[src_ast_file].append({
                        "src_file": src_ast_file,
                        "dst_file": None,
                        "src_stmt": src_stmt_id,
                        "dst_stmt": None,
                        "src_update": {"change_status": change_status},
                        "dst_update": {}
                    })
                    # an updated old statement: its matched new statement changed too
                    if action in ("update-tree", "update-node"):
                        dst_file, dst_stmt_id = counterpart.get(src_stmt_id, (None, None))
                        if dst_stmt_id:
                            change_mapping.setdefault(dst_file or src_ast_file, []).append({
                                "src_file": None,
                                "dst_file": dst_file,
                                "src_stmt": None,
                                "dst_stmt": dst_stmt_id,
                                "src_update": {},
                                "dst_update": {"change_status": "changed"}
                            })

            # Handle move actions (affects both old and new files)
            elif action == "move-tree":
                # Need both src and dst info
                if src_s_info is None:
                    print(f"Warning: src_s_info is None for move-tree change: {change}")
                    continue
                if dst_s_info is None:
                    print(f"Warning: dst_s_info is None for move-tree change: {change}")
                    continue

                src_rel_path = get_relative_path(f"/{src_s_info['file']}", self.root_dir_old)
                dst_rel_path = get_relative_path(f"/{dst_s_info['file']}", self.root_dir_new)
                src_ast_tuple = find_first_matching_tuple(self.old_ast_mapping, src_rel_path, src_s_info["initial_line"])
                dst_ast_tuple = find_first_matching_tuple(self.new_ast_mapping, dst_rel_path, dst_s_info["initial_line"])

                # Fallback to file_arr for global context
                if src_ast_tuple is None and g_ctx and file_arr and len(file_arr) >= 1:
                    old_max_line = max(self.old_line_lookup.keys()) if self.old_line_lookup else 0
                    src_ast_tuple = (0, old_max_line, file_arr[0])

                if dst_ast_tuple is None and g_ctx and file_arr and len(file_arr) >= 2:
                    new_max_line = max(self.new_line_lookup.keys()) if self.new_line_lookup else 0
                    dst_ast_tuple = (0, new_max_line, file_arr[1])

                if src_ast_tuple is None or dst_ast_tuple is None:
                    print(f"Warning: Could not find AST mappings for move-tree change: {change}")
                    continue

                src_ast_file = src_ast_tuple[2]
                dst_ast_file = dst_ast_tuple[2]

                if src_ast_file is None or dst_ast_file is None:
                    continue

                # Load source statements
                if src_ast_file not in self.statement_store:
                    src_code = self.ast_json_objs.get(src_ast_file)
                    if src_code is None:
                        print(f"Warning: AST object not found for source file {src_ast_file}")
                        continue
                    src_stmts = load_statements(src_code.get("statements", []))
                    self.statement_store[src_ast_file] = src_stmts
                else:
                    src_stmts = self.statement_store[src_ast_file]

                # Load destination statements
                if dst_ast_file not in self.statement_store:
                    dst_code = self.ast_json_objs.get(dst_ast_file)
                    if dst_code is None:
                        print(f"Warning: AST object not found for dest file {dst_ast_file}")
                        continue
                    dst_stmts = load_statements(dst_code.get("statements", []))
                    self.statement_store[dst_ast_file] = dst_stmts
                else:
                    dst_stmts = self.statement_store[dst_ast_file]

                # Find matching statements
                src_end_line = src_e_info["initial_line"] if src_e_info else src_s_info["initial_line"]
                dst_end_line = dst_e_info["initial_line"] if dst_e_info else dst_s_info["initial_line"]

                src_stmt_ids = find_most_specific_stmts(
                    src_stmts,
                    (src_s_info["initial_line"], change.get("start_col_old", 0)),
                    (src_end_line, change.get("end_col_old", 0))
                )
                dst_stmt_ids = find_most_specific_stmts(
                    dst_stmts,
                    (dst_s_info["initial_line"], change.get("start_col_new", 0)),
                    (dst_end_line, change.get("end_col_new", 0))
                )

                if not src_stmt_ids or not dst_stmt_ids:
                    continue

                self._note_match_evidence(
                    src_ast_file, src_stmt_ids,
                    (src_s_info["initial_line"], change.get("start_col_old", 0)), (src_end_line, change.get("end_col_old", 0)),
                    dst_ast_file, dst_stmt_ids,
                    (dst_s_info["initial_line"], change.get("start_col_new", 0)), (dst_end_line, change.get("end_col_new", 0)))

                if src_ast_file not in change_mapping:
                    change_mapping[src_ast_file] = []

                # IMPROVED MATCHING LOGIC
                if len(src_stmt_ids) == 1 and len(dst_stmt_ids) == 1:
                    # Simple one-to-one case
                    change_mapping[src_ast_file].append({
                        "src_file": src_ast_file,
                        "dst_file": dst_ast_file,
                        "src_stmt": src_stmt_ids[0],
                        "dst_stmt": dst_stmt_ids[0],
                        "src_update": {"match_id": dst_stmt_ids[0], "change_status": "moved"},
                        "dst_update": {"match_id": src_stmt_ids[0], "change_status": "moved"}
                    })
                else:
                    # Multiple statements case - need smarter matching
                    # Get actual statement objects for comparison
                    src_stmt_objs = []
                    for stmt_id in src_stmt_ids:
                        for s in self.ast_json_objs[src_ast_file].get("statements", []):
                            if s["id"] == stmt_id:
                                src_stmt_objs.append(s)
                                break

                    dst_stmt_objs = []
                    for stmt_id in dst_stmt_ids:
                        for s in self.ast_json_objs[dst_ast_file].get("statements", []):
                            if s["id"] == stmt_id:
                                dst_stmt_objs.append(s)
                                break

                    # Match statements by type and name
                    for src_stmt in src_stmt_objs:
                        matched = False
                        for dst_stmt in dst_stmt_objs:
                            # Skip already matched destination statements
                            if any(entry.get("dst_stmt") == dst_stmt["id"] for entry in change_mapping.get(src_ast_file, [])):
                                continue

                            # Check if statements are compatible
                            if self._are_statements_compatible(src_stmt, dst_stmt):
                                change_mapping[src_ast_file].append({
                                    "src_file": src_ast_file,
                                    "dst_file": dst_ast_file,
                                    "src_stmt": src_stmt["id"],
                                    "dst_stmt": dst_stmt["id"],
                                    "src_update": {"match_id": dst_stmt["id"], "change_status": "moved"},
                                    "dst_update": { "match_id": src_stmt["id"], "change_status": "moved" }
                                })
                                matched = True
                                break

        #logging.info(json.dumps(change_mapping, indent=4))

        return change_mapping
    
    def apply_matching_mapping(self, mapping):
        """
        Apply the matching mapping to the AST nodes of the two versions of the code.
        """
        for src_file, mappings in mapping.items():
            if not mappings:
                continue
            src_file_path = mappings[0]['src_file']
            dst_file_path = mappings[0]['dst_file']

            if src_file_path is None:
                # run through the mapping until mappings[i]['src_file'] is not None
                for i in range(len(mappings)):
                    if mappings[i]['src_file'] is not None:
                        src_file_path = f"{mappings[i]['src_file']}"
                        break
            if dst_file_path is None:
                # run through the mapping until mappings[i]['dst_file'] is not None
                for i in range(len(mappings)):
                    if mappings[i]['dst_file'] is not None:
                        dst_file_path = f"{mappings[i]['dst_file']}"
                        break

            # print(f"Applying mapping for {src_file_path} and {dst_file_path}")

            src_json_data = None
            dst_json_data = None

            if src_file_path in self.ast_json_objs:
                src_json_data = self.ast_json_objs[src_file_path]
            if dst_file_path in self.ast_json_objs:
                dst_json_data = self.ast_json_objs[dst_file_path]

            if src_json_data is None and dst_json_data is None:
                continue

            modified = False

            for entry in mappings:
                src_stmt_id = entry["src_stmt"]
                dst_stmt_id = entry["dst_stmt"]
                src_update = entry.get("src_update", {})
                dst_update = entry.get("dst_update", {})

                # Handle source statement updates
                if "change_status" in src_update and src_json_data is not None:
                    src_statements = src_json_data.get("statements", [])
                    if src_statements:
                        curr_status, match_id = find_stmt_change_status(src_statements, src_stmt_id)
                        src_update["change_status"] = get_higher_priority_status(curr_status, src_update["change_status"])
                        if match_id is not None:
                            src_update["match_id"] = match_id

                # Handle destination statement updates
                if "change_status" in dst_update and dst_json_data is not None:
                    dst_statements = dst_json_data.get("statements", [])
                    if dst_statements:
                        curr_status, match_id = find_stmt_change_status(dst_statements, dst_stmt_id)
                        dst_update["change_status"] = get_higher_priority_status(curr_status, dst_update["change_status"])
                        if match_id is not None:
                            dst_update["match_id"] = match_id

                if src_stmt_id and src_json_data is not None:
                    modified |= find_stmt_and_modify(src_json_data, src_stmt_id, entry["src_update"])

                if dst_stmt_id and dst_json_data is not None:
                    modified |= find_stmt_and_modify(dst_json_data, dst_stmt_id, entry["dst_update"])

            if modified:
                self.ast_json_objs[src_file_path] = src_json_data
                self.ast_json_objs[dst_file_path] = dst_json_data

    def match_stmts(self, g_ctx = False, file_arr=None):
        """
        Match the AST nodes of the two versions of the code.
        """
        stmt_match_mapping = self.matching_stmts(g_ctx, file_arr)
        stmt_change_mapping = self.matching_changes(g_ctx, file_arr, stmt_match_mapping)

        # apply changes in order
        self.apply_matching_mapping(stmt_match_mapping)
        self.apply_matching_mapping(stmt_change_mapping)

        # Post-process to ensure only one match per statement and type correctness
        self._postprocess_matches()
        self._validate_scope_compatibility()

        # logging.info(json.dumps(self.ast_json_objs, indent=4))

        return self.ast_json_objs

    def _postprocess_matches(self):
        """
        After initial matching, ensure that:
        - Only if a statement is matched to more than one statement on the other side, we resolve ambiguity.
        - Always keep one valid match (the best by type and similarity).
        - Prevent self-matching (statement matching to itself).
        """
        # Build reverse maps: id -> [matched_ids]
        stmt_type_map = {}
        stmt_order = {}  # id -> position in the traversal below; the last tie-break, never a set order
        for file_data in self.ast_json_objs.values():
            if file_data is None:
                continue
            for stmt in file_data.get("statements", []):
                stmt_type_map[stmt["id"]] = stmt.get("type")
                stmt_order[stmt["id"]] = len(stmt_order)
        order = lambda sid: stmt_order.get(sid, -1)

        # Collect forward matches only: id -> [match_id] (avoid bidirectional duplication)
        forward_matches = defaultdict(set)
        # Also collect reverse matches to find conflicts
        reverse_matches = defaultdict(set)
        
        for file_data in self.ast_json_objs.values():
            if file_data is None:
                continue
            for stmt in file_data.get("statements", []):
                stmt_id = stmt["id"]
                match_id = stmt.get("match_id")
                if match_id and match_id != stmt_id:  # Prevent self-matching
                    forward_matches[stmt_id].add(match_id)
                    reverse_matches[match_id].add(stmt_id)

        # Find statements with multiple matches (either forward or reverse)
        all_conflicts = set()
        for stmt_id, match_ids in forward_matches.items():
            if len(match_ids) > 1:
                all_conflicts.add(stmt_id)
        for stmt_id, match_ids in reverse_matches.items():
            if len(match_ids) > 1:
                all_conflicts.add(stmt_id)

        # Process each conflicted statement (in source order: ids are random uuids,
        # so the sets above iterate differently from run to run)
        for stmt_id in sorted(all_conflicts, key=order):
            # Get all potential matches for this statement
            potential_matches = forward_matches.get(stmt_id, set()) | reverse_matches.get(stmt_id, set())
            potential_matches = sorted(potential_matches, key=order)
            
            if len(potential_matches) <= 1:
                continue
                
            # Filter out self-matches
            potential_matches = [mid for mid in potential_matches if mid != stmt_id]
            
            if len(potential_matches) <= 1:
                continue
                
            stmt_type = stmt_type_map.get(stmt_id)
            
            # Keep only matches of the same type
            same_type_matches = [mid for mid in potential_matches if stmt_type_map.get(mid) == stmt_type]
            
            if not same_type_matches:
                # If no same-type matches, keep the first valid match
                best = potential_matches[0]
            elif len(same_type_matches) == 1:
                best = same_type_matches[0]
            else:
                # If multiple same-type matches, pick the one with most similar expression
                expr_map = {}
                for file_data in self.ast_json_objs.values():
                    if file_data is None:
                        continue
                    for stmt in file_data.get("statements", []):
                        expr_map[stmt["id"]] = stmt.get("expression", "")
                
                expr = expr_map.get(stmt_id, "")
                # the statement GumTree matched as a whole first (_note_match_evidence),
                # then the most similar expression, then the earliest statement
                best = max(same_type_matches, key=lambda mid: (
                    self.pair_evidence.get((stmt_id, mid), 0),
                    self._calculate_advanced_similarity(expr, expr_map.get(mid, "")),
                    -order(mid)))
            
            # Clear all matches for this statement except the best one
            for file_data in self.ast_json_objs.values():
                if file_data is None:
                    continue
                for stmt in file_data.get("statements", []):
                    current_stmt_id = stmt["id"]
                    current_match_id = stmt.get("match_id")
                    
                    # If this statement is the conflicted one, keep only the best match
                    if current_stmt_id == stmt_id:
                        if current_match_id and current_match_id != best:
                            stmt["match_id"] = best
                            #print(f"Updated match for {stmt_id}: changed from {current_match_id} to {best}")
                    
                    # If this statement was matched to the conflicted one but isn't the best, clear it
                    elif current_match_id == stmt_id and current_stmt_id != best:
                        stmt["match_id"] = None
                        #print(f"Cleared match_id for {current_stmt_id} as it was matched to {stmt_id}, but {best} was chosen as best match")
                    
                    # If this statement is one of the potential matches but not the best, clear its reverse match
                    elif current_stmt_id in potential_matches and current_stmt_id != best and current_match_id == stmt_id:
                        stmt["match_id"] = None
                        #print(f"Cleared reverse match for {current_stmt_id} as {best} was chosen as best match for {stmt_id}")

    def _validate_scope_compatibility(self):
        """
        Validate that matched statements are in compatible scopes.
        If statements from different scope levels are matched, break the match
        and mark them as deleted/inserted instead.
        """
        # Build a map of statement_id -> scope information
        stmt_scope_map = {}
        stmt_file_map = {}
        
        for file_key, file_data in self.ast_json_objs.items():
            if file_data is None:
                continue
            for stmt in file_data.get("statements", []):
                stmt_id = stmt["id"]
                stmt_scope_map[stmt_id] = {
                    "scope_depth": stmt.get("scope_depth", 0),
                    "scope_id": stmt.get("scope_id", 0),
                    "scope_level": stmt.get("scope_level", 0),
                    "type": stmt.get("type", ""),
                    "expression": stmt.get("expression", "")
                }
                stmt_file_map[stmt_id] = file_key
        
        # Find all matched pairs and validate scope compatibility
        matches_to_break = []
        
        for file_key, file_data in self.ast_json_objs.items():
            if file_data is None:
                continue
            for stmt in file_data.get("statements", []):
                stmt_id = stmt["id"]
                match_id = stmt.get("match_id")
                change_status = stmt.get("change_status", "")
                
                if not match_id or change_status not in ["matched", "changed"]:
                    continue
                
                # Get scope information for both statements
                src_scope = stmt_scope_map.get(stmt_id)
                dst_scope = stmt_scope_map.get(match_id)
                
                if not src_scope or not dst_scope:
                    continue
                
                # Check if scopes are incompatible
                if self._are_scopes_incompatible(src_scope, dst_scope, stmt_id, match_id):
                    matches_to_break.append((stmt_id, match_id, file_key, stmt_file_map.get(match_id)))
        
        # Break incompatible matches
        for src_stmt_id, dst_stmt_id, src_file, dst_file in matches_to_break:
            self._break_match(src_stmt_id, dst_stmt_id, src_file, dst_file)
    
    def _are_scopes_incompatible(self, src_scope, dst_scope, src_stmt_id, dst_stmt_id):
        """
        Determine if two scopes are incompatible for matching.
        Only break matches in extreme cases where scope difference indicates 
        completely different contexts (e.g., different functions entirely).
        
        Args:
            src_scope: Scope info for source statement
            dst_scope: Scope info for destination statement
            src_stmt_id: Source statement ID for debugging
            dst_stmt_id: Destination statement ID for debugging
        
        Returns:
            True if scopes are incompatible and match should be broken
        """
        # Get scope depths
        src_depth = src_scope.get("scope_depth", 0)
        dst_depth = dst_scope.get("scope_depth", 0)
        
        # Only break matches for EXTREME scope differences (5+ levels)
        # This catches cases where statements are matched across completely different contexts
        extreme_scope_difference = 5
        
        if abs(src_depth - dst_depth) > extreme_scope_difference:
            # This is likely a false match across different functions/classes
            print(f"Breaking match {src_stmt_id} <-> {dst_stmt_id}: extreme scope difference ({src_depth} vs {dst_depth})")
            return True
        
        # Additional check: if expressions are completely different AND scope differs significantly,
        # it might be a false match
        src_expr = src_scope.get("expression", "").strip()
        dst_expr = dst_scope.get("expression", "").strip()
        
        if (abs(src_depth - dst_depth) >= 3 and src_expr and dst_expr and 
            len(src_expr) > 10 and len(dst_expr) > 10):  # Only for non-trivial expressions
            
            # Very strict similarity check - only break if expressions are completely different
            src_words = set(src_expr.lower().split())
            dst_words = set(dst_expr.lower().split())
            
            if src_words and dst_words:
                similarity = len(src_words.intersection(dst_words)) / max(len(src_words), len(dst_words))
                
                # Only break if similarity is extremely low (< 0.1) and scope difference is large
                if similarity < 0.1 and abs(src_depth - dst_depth) >= 4:
                    print(f"Breaking match {src_stmt_id} <-> {dst_stmt_id}: very low similarity ({similarity:.2f}) with large scope difference ({src_depth} vs {dst_depth})")
                    return True
        
        return False
    
    def _break_match(self, src_stmt_id, dst_stmt_id, src_file, dst_file):
        """
        Break a match between two statements and mark them as deleted/inserted.
        """
        # Find and update source statement
        if src_file and src_file in self.ast_json_objs:
            src_file_data = self.ast_json_objs[src_file]
            if src_file_data:
                for stmt in src_file_data.get("statements", []):
                    if stmt["id"] == src_stmt_id:
                        stmt["change_status"] = "deleted"
                        if "match_id" in stmt:
                            del stmt["match_id"]
                        break
        
        # Find and update destination statement
        if dst_file and dst_file in self.ast_json_objs:
            dst_file_data = self.ast_json_objs[dst_file]
            if dst_file_data:
                for stmt in dst_file_data.get("statements", []):
                    if stmt["id"] == dst_stmt_id:
                        stmt["change_status"] = "inserted"
                        if "match_id" in stmt:
                            del stmt["match_id"]
                        break

    def _calculate_advanced_similarity(self, expr_a, expr_b):
        """
        Calculate advanced similarity between two expressions using:
        1. Common coherent character sequences (substrings)
        2. Length factor to penalize very different lengths
        3. Number and length of matching sequences
        
        Args:
            expr_a: First expression string
            expr_b: Second expression string
            
        Returns:
            float: Similarity score between 0 and 1
        """
        if not expr_a or not expr_b:
            return 0.0
        
        # Normalize whitespace and case for comparison
        a = ' '.join(expr_a.strip().split())
        b = ' '.join(expr_b.strip().split())
        
        if not a or not b:
            return 0.0
            
        if a == b:
            return 1.0
        
        # Find all common substrings of length >= 3
        common_sequences = []
        min_seq_length = 3
        
        # Use dynamic programming to find longest common substrings
        for i in range(len(a)):
            for j in range(len(b)):
                # Find the length of common substring starting at i, j
                k = 0
                while (i + k < len(a) and j + k < len(b) and 
                       a[i + k] == b[j + k]):
                    k += 1
                
                # If we found a sequence of meaningful length, record it
                if k >= min_seq_length:
                    sequence = a[i:i+k]
                    # Avoid overlapping sequences by checking if this sequence
                    # is already covered by a longer one
                    is_subset = False
                    for existing_seq in common_sequences:
                        if sequence in existing_seq:
                            is_subset = True
                            break
                    
                    if not is_subset:
                        # Remove any existing sequences that are subsets of this one
                        common_sequences = [seq for seq in common_sequences if seq not in sequence]
                        common_sequences.append(sequence)
        
        # Calculate similarity components
        total_common_length = sum(len(seq) for seq in common_sequences)
        num_sequences = len(common_sequences)
        max_length = max(len(a), len(b))
        min_length = min(len(a), len(b))
        
        # Length penalty: penalize if lengths are very different
        length_ratio = min_length / max_length if max_length > 0 else 0
        length_penalty = 0.8 + 0.2 * length_ratio  # Between 0.8 and 1.0
        
        # Base similarity: ratio of common characters to total length
        base_similarity = total_common_length / max_length if max_length > 0 else 0
        
        # Sequence bonus: reward for having multiple coherent sequences
        sequence_bonus = 1.0 + (num_sequences * 0.1)  # Small bonus for each sequence
        
        # Calculate average sequence length (longer sequences are better)
        avg_sequence_length = total_common_length / num_sequences if num_sequences > 0 else 0
        sequence_quality = min(1.0, avg_sequence_length / 10)  # Normalize by expected length
        
        # Combine all factors
        similarity = base_similarity * length_penalty * sequence_bonus * (1 + sequence_quality * 0.2)
        
        # Cap at 1.0
        return min(1.0, similarity)