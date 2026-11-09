import sys
import json
import os
import hashlib

# Add the project root to Python path

from crossslice.intra.general_code_analyzer import create_ast_json_global, create_ast_json
from crossslice.intra.gumtree_handler import create_gumtree_diff, map_changes_to_lines, map_matches_to_lines
from crossslice.intra.matching import NodeMatcher
from crossslice.intra.pre_merge import run_through_stmts
from crossslice.intra.relevant_dataflow import find_relevant_dataflow, mark_statements_between_moved_positions
from crossslice.intra.merge import merge_statements
from crossslice.intra.formatter import Formatter

CHANGE_PRIORITY = {
    "changed": 5,
    "deleted": 4,
    "inserted": 3,
    "moved": 2,
    "matched": 1
}

def has_actual_changes(merged_statements):
    """
    Check if merged statements contain any actual AST-level changes.

    Whitespace-only changes (like trailing space removal or empty line changes)
    don't show up in the AST, so the merge result will only contain 'matched'
    statements if there are no real code changes.

    Args:
        merged_statements: List of merged statement dictionaries

    Returns:
        True if there are actual changes (changed/deleted/inserted/moved),
        False if all statements are just 'matched' (whitespace-only change)
    """
    if not merged_statements:
        return False

    for stmt in merged_statements:
        change_status = stmt.get('change_status', 'matched')
        if change_status in ('changed', 'deleted', 'inserted', 'moved', 'moved_from'):
            return True

    return False

def get_relative_path(file_path, root_dir):
    """
    Get the relative path of a file from a root directory
    """
    return os.path.relpath(file_path, root_dir)

def create_short_hash(input_string):
    """
    Genereate short hash for given input string
    """
    return hashlib.md5(input_string.encode()).hexdigest()[:6]

def build_line_lookup_global(diff_data, old_file, new_file):
    """
    Build line lookup dictionaries for global context.

    For global context, we map each line to itself (no offset needed) since
    the global context file is the complete file, not an extracted function.

    Args:
        diff_data: Dictionary containing 'old_lines' and 'new_lines' lists
        old_file: Path to the old version file
        new_file: Path to the new version file

    Returns:
        Tuple of (old_line_lookup, new_line_lookup) dictionaries
    """
    old_line_lookup = {}
    new_line_lookup = {}

    # The lookup must cover the WHOLE file, not just the lines up to the last
    # diff hunk: GumTree matches of statements after the last change are
    # otherwise dropped by the matcher, and everything below an insertion is
    # reported as deleted + re-inserted.
    old_lines = diff_data.get("old_lines", [])
    old_max_from_code = (diff_data.get("old_code") or "").count("\n")
    if (old_lines and len(old_lines) > 0) or old_max_from_code:
        max_old_line = max(old_lines[-1] if old_lines else 0, old_max_from_code)
        for line in range(0, max_old_line + 1):
            old_line_lookup[line] = {
                "initial_line": line,
                "file": old_file,
                "type": "old",
                "function": "__global_context__",
            }
    else:
        # If no old lines, create at least line 0 to avoid empty lookup issues
        # This happens when the old file is /dev/null (new file added)
        if old_file and old_file != "/dev/null":
            old_line_lookup[0] = {
                "initial_line": 0,
                "file": old_file,
                "type": "old",
                "function": "__global_context__",
            }

    new_lines = diff_data.get("new_lines", [])
    new_max_from_code = (diff_data.get("new_code") or "").count("\n")
    if (new_lines and len(new_lines) > 0) or new_max_from_code:
        max_new_line = max(new_lines[-1] if new_lines else 0, new_max_from_code)
        for line in range(0, max_new_line + 1):
            new_line_lookup[line] = {
                "initial_line": line,
                "file": new_file,
                "type": "new",
                "function": "__global_context__",
            }
    else:
        # If no new lines, create at least line 0 to avoid empty lookup issues
        # This happens when the new file is /dev/null (file deleted)
        if new_file and new_file != "/dev/null":
            new_line_lookup[0] = {
                "initial_line": 0,
                "file": new_file,
                "type": "new",
                "function": "__global_context__",
            }

    return old_line_lookup, new_line_lookup

def build_line_lookup_func(diff_data, func_name, file):
    old_line_lookup = {}
    new_line_lookup = {}

    for new_file, file_data in diff_data.items():
        old_file = file_data["old_file"]
        new_file = file_data["new_file"]

        if old_file != file and new_file != file:
            continue

        for function_name, function_data in file_data["functions"].items():
            if function_name != func_name:
                continue

            old_mapped_start, old_mapped_end = function_data.get("old_mapped_lines") if function_data.get("old_mapped_lines") != [] else [None, None]
            old_initial_start, old_initial_end = function_data.get("old_initial_lines") if function_data.get("old_initial_lines") != [] else [None, None]

            new_mapped_start, new_mapped_end = function_data.get("new_mapped_lines") if function_data.get("new_mapped_lines") != [] else [None, None]
            new_initial_start, new_initial_end = function_data.get("new_initial_lines") if function_data.get("new_initial_lines") != [] else [None, None]

            # Compute offsets (if valid)
            if old_mapped_start is not None and old_initial_start is not None:
                old_offset = old_initial_start - old_mapped_start
                for line in range(old_mapped_start, old_mapped_end + 1):
                    old_line_lookup[line] = {
                        "initial_line": line + old_offset,
                        "file": old_file,
                        "type": "old",
                        "function": function_name,
                    }

            if new_mapped_start is not None and new_initial_start is not None:
                new_offset = new_initial_start - new_mapped_start
                for line in range(new_mapped_start, new_mapped_end + 1):
                    new_line_lookup[line] = {
                        "initial_line": line + new_offset,
                        "file": new_file,
                        "type": "new",
                        "function": function_name,
                    }
    return old_line_lookup, new_line_lookup

def propagate_via_part_of(statements):
    """
    For each statement S with no change_status:
      1) If S.additional_info contains {'part_of': part_id}, then
         let P = the statement whose parts list includes that part_id.
         If P.change_status is a real change, set S.change_status = P.change_status.
      2) Else if S has no status, inherit statements[i-1].change_status (if any).
    This ensures that every inner statement under a changed control-flow 
    node gets the same change_status, using your existing part links.
    """
    # 1) Build part_id -> parent_statement mapping
    part_owner = {}
    for stmt in statements:
        for part in stmt.get("parts", []):
            pid = part["id"]
            part_owner[pid] = stmt

    # 2) Walk in source order
    for i, stmt in enumerate(statements):
        cs = stmt.get("change_status")
        if cs:  # already has a real status (even "matched"), skip
            continue

        # a) try part_of inheritance
        inherited = None
        for info in stmt.get("additional_info", []):
            if isinstance(info, dict) and "part_of" in info:
                pid = info["part_of"]
                parent = part_owner.get(pid)
                if parent:
                    pstatus = parent.get("change_status")
                    if pstatus and pstatus != "matched":
                        inherited = pstatus
                        break

        # b) fallback: inherit previous stmt’s status
        if inherited is None and i > 0:
            prev_cs = statements[i - 1].get("change_status")
            if prev_cs and prev_cs != "matched":
                inherited = prev_cs

        # c) assign if found
        if inherited:
            stmt["change_status"] = inherited

    return statements


def gen_dataflow(changes, root_dir_old, root_dir_new, level=2, collect_internals=False):
    """
    Generate data flow from the changes in the source code.

    With collect_internals=True, returns (dataflow_text, internals) where
    internals is a list of {"mapping", "merged", "old_data", "new_data"} per
    emitted function block — the input the cross-function enricher consumes.
    """
    old_ast_mapping = {}
    new_ast_mapping = {}

    ast_json_mapping = []
    ast_json_objs = {}

    # For each change, create the AST
    for file, details in changes.items():
        file_path_old = f"/{details['old_file']}"
        file_path_new = f"/{details['new_file']}"
        relative_old = get_relative_path(f"/{details['old_file']}", root_dir_old) if details["old_file"] != "/dev/null" else None
        relative_new = get_relative_path(f"/{details['new_file']}", root_dir_new) if details["new_file"] != "/dev/null" else None

        old_dir, old_file = os.path.split(file_path_old)
        old_name, _ = os.path.splitext(old_file)
        new_dir, new_file = os.path.split(file_path_new)
        new_name, _ = os.path.splitext(new_file)
        old_ast_path = f"{old_dir}/{old_name}_{create_short_hash(relative_old)}" if relative_old else None
        new_ast_path = f"{new_dir}/{new_name}_{create_short_hash(relative_new)}" if relative_new else None

        #
        # ────────────────────────────────────────────────────────────────────────────────
        #  Handle global context
        # ────────────────────────────────────────────────────────────────────────────────
        #
        global_context_function = details["functions"].get("__global_context__", {})
        if global_context_function:
            old_ast_file = f"{old_ast_path}_global" if old_ast_path else None
            new_ast_file = f"{new_ast_path}_global" if new_ast_path else None

            # Initialize temp variables to None before conditional assignment
            temp_old = None
            temp_new = None

            if global_context_function.get("old_file_path"):
                try:
                    temp_old = create_ast_json_global(global_context_function["old_file_path"])
                except Exception as e:
                    print(f"Warning: Failed to create AST for old global context in {file}: {e}")
                    temp_old = None

            if global_context_function.get("new_file_path"):
                try:
                    temp_new = create_ast_json_global(global_context_function["new_file_path"])
                except Exception as e:
                    print(f"Warning: Failed to create AST for new global context in {file}: {e}")
                    temp_new = None

            # Store AST objects (only if we have valid file keys)
            if old_ast_file:
                ast_json_objs[old_ast_file] = temp_old
            if new_ast_file:
                ast_json_objs[new_ast_file] = temp_new

            # Add to mapping only if we have at least one valid AST file
            if old_ast_file or new_ast_file:
                ast_json_mapping.append({
                    "old": old_ast_file,
                    "new": new_ast_file,
                    "old_relative_path": relative_old,
                    "new_relative_path": relative_new,
                })

            # Skip matching if either file path is missing
            if global_context_function.get("old_file_path") is None or global_context_function.get("new_file_path") is None:
                print(f"Skipping __global_context__ matching in file {file} due to missing file paths.")
            elif temp_old is None or temp_new is None:
                print(f"Skipping __global_context__ matching in file {file} due to AST creation failure.")
            else:
                # Both file paths exist and ASTs were created successfully
                try:
                    gum_changes, gum_matches, line_offsets_a, line_offsets_b = create_gumtree_diff(
                        global_context_function.get("old_file_path"),
                        global_context_function.get("new_file_path"),
                        global_context_function.get("old_code"),
                        global_context_function.get("new_code")
                    )
                except Exception as e:
                    print(f"Warning: GumTree diff failed for global context in {file}: {e}")
                    gum_changes, gum_matches = [], []
                    # Create empty line offsets based on the code
                    old_code = global_context_function.get("old_code", "")
                    new_code = global_context_function.get("new_code", "")
                    line_offsets_a = [0] + [i + 1 for i, c in enumerate(old_code) if c == '\n']
                    line_offsets_b = [0] + [i + 1 for i, c in enumerate(new_code) if c == '\n']

                changes_mapping = map_changes_to_lines(gum_changes, line_offsets_a, line_offsets_b, gum_matches)  # 0-based line numbers
                matches_mapping = map_matches_to_lines(gum_matches, line_offsets_a, line_offsets_b)  # 0-based line numbers
                old_line_lookup, new_line_lookup = build_line_lookup_global(
                    global_context_function,
                    global_context_function["old_file_path"],
                    global_context_function["new_file_path"]
                )  # 0-based line numbers

                # IMPORTANT: Add global context to AST mappings so NodeMatcher can find them
                # Global context spans from line 0 to the last line of the file
                old_max_line = max(old_line_lookup.keys()) if old_line_lookup else 0
                new_max_line = max(new_line_lookup.keys()) if new_line_lookup else 0

                if relative_old and old_ast_file:
                    if relative_old not in old_ast_mapping:
                        old_ast_mapping[relative_old] = []
                    old_ast_mapping[relative_old].append((0, old_max_line, old_ast_file))

                if relative_new and new_ast_file:
                    if relative_new not in new_ast_mapping:
                        new_ast_mapping[relative_new] = []
                    new_ast_mapping[relative_new].append((0, new_max_line, new_ast_file))

                # Use enhanced NodeMatcher with global context flag
                matcher = NodeMatcher(
                    matches_mapping, changes_mapping,
                    old_line_lookup, new_line_lookup,
                    old_ast_mapping, new_ast_mapping,
                    root_dir_old, root_dir_new, ast_json_objs
                )
                ast_json_objs = matcher.match_stmts(g_ctx=True, file_arr=[old_ast_file, new_ast_file])

        for function in details["functions"]:
            if function == "__global_context__":
                continue
            # Get functions start and end line
            old_start, old_end = details["functions"][function].get("old_initial_lines", [None, None]) if details["functions"][function]["old_initial_lines"] != [] else [None, None]
            new_start, new_end = details["functions"][function].get("new_initial_lines", [None, None]) if details["functions"][function]["new_initial_lines"] != [] else [None, None]

            old_ast_file = f"{old_ast_path}_{old_start}_{old_end}"
            new_ast_file = f"{new_ast_path}_{new_start}_{new_end}"
            
            if relative_old in old_ast_mapping:
                old_ast_mapping[relative_old].append((old_start, old_end, old_ast_file))
            else:
                old_ast_mapping[relative_old] = [(old_start, old_end, old_ast_file)]

            if relative_new in new_ast_mapping:
                new_ast_mapping[relative_new].append((new_start, new_end, new_ast_file))
            else:
                new_ast_mapping[relative_new] = [(new_start, new_end, new_ast_file)]

            old_line = old_start if old_start is not None else None
            new_line = new_start if new_start is not None else None
            
            if old_line is not None:
                temp_old = create_ast_json(file_path_old, old_line)
                ast_json_objs[old_ast_file] = temp_old
            else:
                ast_json_objs[old_ast_file] = None

            if new_line is not None:
                temp_new = create_ast_json(file_path_new, new_line)
                ast_json_objs[new_ast_file] = temp_new
            else:
                ast_json_objs[new_ast_file] = None

            ast_json_mapping.append({
                "old": old_ast_file,
                "new": new_ast_file,
                "old_relative_path": relative_old,
                "new_relative_path": relative_new,
            })


            f_old = details["functions"][function].get("old_file_path", None)
            f_new = details["functions"][function].get("new_file_path", None)
            old_code = details["functions"][function].get("old_code", None)
            new_code = details["functions"][function].get("new_code", None)

            if f_old is None or f_new is None:
                print(f"Skipping function {function} in file {file} due to missing file paths.")
                continue

            gum_changes, gum_matches, line_offsets_a, line_offsets_b = create_gumtree_diff(f_old, f_new, old_code, new_code)
            changes_mapping = map_changes_to_lines(gum_changes, line_offsets_a, line_offsets_b, gum_matches) # 0-based line numbers
            matches_mapping = map_matches_to_lines(gum_matches, line_offsets_a, line_offsets_b) # 0-based line numbers
            old_line_lookup, new_line_lookup = build_line_lookup_func(changes, function, file) # 0-based line numbers

            # Use enhanced NodeMatcher with None handling
            matcher = NodeMatcher(matches_mapping, changes_mapping, old_line_lookup, new_line_lookup, old_ast_mapping, new_ast_mapping, root_dir_old, root_dir_new, ast_json_objs)
            ast_json_objs = matcher.match_stmts()

            print(f"Processed function {function} in file {file}")

    dataflow_text = ""
    dataflow_json = {}

    dataflow_word_level = ""
    internals = []

    counter = 1

    for obj in ast_json_mapping:
        old_data = ast_json_objs[obj["old"]] if obj["old"] in ast_json_objs else None
        new_data = ast_json_objs[obj["new"]] if obj["new"] in ast_json_objs else None

        if old_data:
            old_data["statements"] = propagate_via_part_of(old_data["statements"])
        if new_data:
            new_data["statements"] = propagate_via_part_of(new_data["statements"])

        old_stmts = run_through_stmts(old_data["statements"]) if old_data else None
        new_stmts = run_through_stmts(new_data["statements"]) if new_data else None


        # --------------------------------
        if old_stmts:
            old_stmts = find_relevant_dataflow(old_stmts, level=level)
        if new_stmts:
            new_stmts = find_relevant_dataflow(new_stmts, level=level)

        # # append the old_stmts to a json file (create the file if it does not exist)
        # if old_stmts:
        #    with open(f"./logs/old_stmts_{counter}.json", "w") as f:
        #        json.dump(old_stmts, f, indent=4)

        # # append the new_stmts to a json file (create the file if it does not exist)
        # if new_stmts:
        #    with open(f"./logs/new_stmts_{counter}.json", "w") as f:
        #        json.dump(new_stmts, f, indent=4)

        if not old_stmts and not new_stmts:
            # e.g. changed regions that are not functions (macro-generated test
            # bodies, file-level declarations): nothing to slice in either version
            print(f"Skipping {obj.get('function_name', 'unknown')} - no analyzable statements in either version")
            counter += 1
            continue

        merged, var_mapping = merge_statements(old_stmts, new_stmts)

        # Filter out whitespace-only changes (functions where all statements are just 'matched')
        if not has_actual_changes(merged):
            print(f"Skipping {obj.get('function_name', 'unknown')} - no AST-level changes (whitespace-only)")
            counter += 1
            continue

        # Mark statements between moved positions as relevant
        # This needs to run on merged statements (which have both ghost and moved)
        merged = mark_statements_between_moved_positions(merged)

        if collect_internals:
            internals.append({
                "mapping": obj,
                "merged": merged,
                "old_data": old_data,
                "new_data": new_data,
            })

        # # Save variable mapping for reference
        # with open(f"./logs/var_mapping_{counter}.json", 'w') as f:
        #     json.dump(var_mapping, f, indent=2)
        print(f"Variable mapping saved to var_mapping_{counter}.json")

        counter += 1

        # # # write merged to file
        # with open(f"./logs/merged_{counter}.json", "w") as f:
        #    json.dump(merged, f, indent=4)


        formatter = Formatter(language="c", merged_statements=merged)
        formatted_text = formatter.format_git_diff_style()

        # formatted text on word level
        formatted_text_word_level = formatter.format_merged_statements(diff_format="word")
        dataflow_word_level += f"Context for merged statement of old file: {obj['old_relative_path']} with new file: {obj['new_relative_path']}:\n{formatted_text_word_level}\n\n"

        #--------------------
        dataflow_text += f"Context for merged statement of old file: {obj['old_relative_path']} with new file: {obj['new_relative_path']}:\n{formatted_text}\n\n"

        if obj["new_relative_path"] in dataflow_json:
           dataflow_json[obj["new_relative_path"]].append(formatted_text)
        else:
           dataflow_json[obj["new_relative_path"]] = [formatted_text]

    print(dataflow_word_level)

    if collect_internals:
        return dataflow_text, internals
    return dataflow_text