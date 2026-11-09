import os
import shutil
import sys
import json
import subprocess
import re

# Add the project root to Python path

def build_line_index(source_code):
    """
    Returns a list `line_offsets` where line_offsets[i] is the
    cumulative number of characters (including newline) up to the
    start of line i (0-based).
    """
    lines = source_code.splitlines(True)  # Keep newline chars
    line_offsets = [0]
    running_offset = 0
    
    for line in lines:
        running_offset += len(line)
        line_offsets.append(running_offset)
    
    return line_offsets

def offset_to_line_col(offset, line_offsets):
    """
    Given a character offset and the line_offsets array,
    returns (line_number, column_number) 0-based.
    """
    line_num = 0
    while line_num < len(line_offsets) - 1 and line_offsets[line_num+1] <= offset:
        line_num += 1
    
    col_num = offset - line_offsets[line_num]
    
    return line_num, col_num

def create_gumtree_diff(file_source, file_dest, src_code, dst_code):
    """
    Create a diff between two files using GumTree and return the changes mapping.

    Args:
        file_source: Path to the source (old) file
        file_dest: Path to the destination (new) file
        src_code: Source code content of old file
        dst_code: Source code content of new file

    Returns:
        Tuple of (changes, matches, line_offsets_a, line_offsets_b)
        Returns empty lists for changes/matches if GumTree fails.

    Raises:
        FileNotFoundError: If GumTree binary is not found
    """
    # GUMTREE_PATH, `gumtree` on PATH, or a release unpacked in a usual place
    from crossslice.paths import find_gumtree, MissingTool
    PATH_GUMTREE = find_gumtree() or ""
    if not PATH_GUMTREE or not os.path.exists(PATH_GUMTREE):
        raise MissingTool(
            "GumTree binary not found. Unzip the GumTree 4.0.0-beta3 release (needs Java 17+) "
            "into /opt/gumtree or ~/gumtree, or set GUMTREE_PATH to its bin/gumtree, or put "
            "`gumtree` on PATH. See scripts/setup_tools.sh or use the Docker image.")

    # Build line indices regardless of GumTree outcome
    line_offsets_a = build_line_index(src_code if src_code else "")
    line_offsets_b = build_line_index(dst_code if dst_code else "")

    print(f"Running command: {PATH_GUMTREE} textdiff -m gumtree-classic-theta -g c-treesitter-ng -f JSON {file_source} {file_dest}")

    try:
        result = subprocess.run(
            [
                PATH_GUMTREE,
                "textdiff",
                "-m", "gumtree-classic-theta",
                "-g", "c-treesitter-ng",
                "-f", "JSON",
                file_source, file_dest
            ],
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )

        # Check for subprocess errors
        if result.returncode != 0:
            print(f"Warning: GumTree exited with code {result.returncode}")
            if result.stderr:
                print(f"GumTree stderr: {result.stderr[:500]}")  # Limit stderr output
            return [], [], line_offsets_a, line_offsets_b

        # Check for empty output
        if not result.stdout or not result.stdout.strip():
            print(f"Warning: GumTree returned empty output for {file_source} -> {file_dest}")
            return [], [], line_offsets_a, line_offsets_b

        # Parse JSON output
        try:
            json_output = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse GumTree JSON output: {e}")
            print(f"GumTree stdout (first 500 chars): {result.stdout[:500]}")
            return [], [], line_offsets_a, line_offsets_b

        # Extract changes and matches with safe access
        changes = json_output.get('actions', [])
        matches = json_output.get('matches', [])

        return changes, matches, line_offsets_a, line_offsets_b

    except subprocess.TimeoutExpired:
        print(f"Warning: GumTree timed out after 60 seconds for {file_source} -> {file_dest}")
        return [], [], line_offsets_a, line_offsets_b

    except Exception as e:
        print(f"Warning: Unexpected error running GumTree: {e}")
        return [], [], line_offsets_a, line_offsets_b

def is_comment_only_change(details):
    """
    Check if a GumTree change action is only affecting comments.
    GumTree tree format is: "node_type: content [start,end]" or "node_type [start,end]"
    """
    tree = details.get("tree", "")
    # Check if the tree starts with "comment:" or "comment ["
    if tree.startswith("comment:") or tree.startswith("comment ["):
        return True
    return False


def map_changes_to_lines(changes, line_offsets_a, line_offsets_b, matches=None):
    """
    Map the changes of gumtree to the line numbers in the original files.
    Filters out comment-only changes since they don't affect the actual code.

    Args:
        changes: List of GumTree actions
        line_offsets_a: Line offsets for source (old) file
        line_offsets_b: Line offsets for destination (new) file
        matches: List of GumTree matches (used to find new position for move-tree)
    """
    changes_mapping = []
    char_range_pattern = re.compile(r"\[(\d+),(\d+)\]")

    # Build a lookup for matches: old_tree_spec -> new_tree_spec
    match_lookup = {}
    if matches:
        for match in matches:
            src = match.get("src", "")
            dest = match.get("dest", "")
            if src and dest:
                match_lookup[src] = dest

    for details in changes:
        # Skip comment-only changes - they don't affect actual code
        if is_comment_only_change(details):
            continue
        if details["action"] == "insert-tree" or details["action"] == "insert-node":
            # New line inserted
            inserted_tree = details["tree"]
            start_char, end_char = char_range_pattern.search(inserted_tree).groups()
            start_line, start_col = offset_to_line_col(int(start_char), line_offsets_b)
            end_line, end_col = offset_to_line_col(int(end_char), line_offsets_b)
            changes_mapping.append({
                "action": "insert-tree" if details["action"] == "insert-tree" else "insert-node",
                "start_line": start_line,
                "end_line": end_line,
                "start_col": start_col,
                "end_col": end_col
            })
        elif details["action"] == "move-tree":
            tree_old_v = details["tree"]

            # Get the old tree range
            start_char, end_char = char_range_pattern.search(tree_old_v).groups()
            start_line_old, start_col_old = offset_to_line_col(int(start_char), line_offsets_a)
            end_line_old, end_col_old = offset_to_line_col(int(end_char), line_offsets_a)

            # Find the new position from matches (NOT from parent!)
            # The parent field in move-tree is the NEW parent node, not the moved node's new position
            tree_new_v = match_lookup.get(tree_old_v)

            if tree_new_v:
                # Found the match - use it to get the new position
                match_result = char_range_pattern.search(tree_new_v)
                if match_result:
                    start_char_new, end_char_new = match_result.groups()
                    start_line_new, start_col_new = offset_to_line_col(int(start_char_new), line_offsets_b)
                    end_line_new, end_col_new = offset_to_line_col(int(end_char_new), line_offsets_b)
                else:
                    # Match found but no position - skip this change
                    print(f"Warning: Could not parse position from match: {tree_new_v}")
                    continue
            else:
                # Fallback: use parent (this is wrong but better than nothing)
                print(f"Warning: No match found for move-tree: {tree_old_v}, using parent (may be incorrect)")
                tree_parent = details["parent"]
                start_char_new, end_char_new = char_range_pattern.search(tree_parent).groups()
                start_line_new, start_col_new = offset_to_line_col(int(start_char_new), line_offsets_b)
                end_line_new, end_col_new = offset_to_line_col(int(end_char_new), line_offsets_b)

            changes_mapping.append({
                "action": "move-tree",
                "start_line_old": start_line_old,
                "end_line_old": end_line_old,
                "start_col_old": start_col_old,
                "end_col_old": end_col_old,
                "start_line_new": start_line_new,
                "end_line_new": end_line_new,
                "start_col_new": start_col_new,
                "end_col_new": end_col_new
            })
        elif details["action"] == "delete-tree" or details["action"] == "delete-node":
            deleted_tree = details["tree"]
            start_char, end_char = char_range_pattern.search(deleted_tree).groups()
            start_line, start_col = offset_to_line_col(int(start_char), line_offsets_a)
            end_line, end_col = offset_to_line_col(int(end_char), line_offsets_a)
            changes_mapping.append({
                "action": "delete-tree" if details["action"] == "delete-tree" else "delete-node",
                "start_line": start_line,
                "end_line": end_line,
                "start_col": start_col,
                "end_col": end_col
            })
        elif details["action"] == "update-tree" or details["action"] == "update-node":
            tree = details["tree"]
            start_char, end_char = char_range_pattern.search(tree).groups()
            start_line, start_col = offset_to_line_col(int(start_char), line_offsets_a)
            end_line, end_col = offset_to_line_col(int(end_char), line_offsets_a)
            changes_mapping.append({
                "action": "update-tree" if details["action"] == "update-tree" else "update-node",
                "start_line": start_line,
                "end_line": end_line,
                "start_col": start_col,
                "end_col": end_col
            })
        else:
            raise ValueError(f"Unknown action: {details['action']}, details: {details}")
        
    # sort the changes based on the start line; the remaining keys make the
    # order total, so GumTree's own list order (which varies between runs of
    # the same input) cannot leak into the matching
    changes_mapping.sort(key=lambda x: (
        x.get("start_line", x.get("start_line_new", float('inf'))),
        x.get("start_col", x.get("start_col_new", float('inf'))),
        x.get("end_line", x.get("end_line_new", float('inf'))),
        x.get("end_col", x.get("end_col_new", float('inf'))),
        x["action"],
        x.get("start_line_old", -1), x.get("start_col_old", -1),
        x.get("end_line_old", -1), x.get("end_col_old", -1),
    ))

    return changes_mapping

def map_matches_to_lines(matches, line_offsets_a, line_offsets_b):
    """
    Map the matches of gumtree to the line numbers in the original files
    """
    matches_mapping = []
    char_range_pattern = re.compile(r"\[(\d+),(\d+)\]")
    for match in matches:
        src_str = match["src"]
        dst_str = match["dest"]

        # Skip high-level structural matches that are likely to cause problems
        if ("compound_statement" in src_str or "function_definition" in src_str or 
            "compound_statement" in dst_str or "function_definition" in dst_str):
            # Skip unless this is a very specific match (e.g., a simple statement)
            src_lines = src_str.count('\n')
            dst_lines = dst_str.count('\n')
            
            # If it spans multiple lines, it's probably a high-level structure
            if src_lines > 1 or dst_lines > 1:
                continue

        src_start, src_end = char_range_pattern.search(src_str).groups()
        dst_start, dst_end = char_range_pattern.search(dst_str).groups()
        src_start_line, src_start_col = offset_to_line_col(int(src_start), line_offsets_a)
        src_end_line, src_end_col = offset_to_line_col(int(src_end), line_offsets_a)
        dst_start_line, dst_start_col = offset_to_line_col(int(dst_start), line_offsets_b)
        dst_end_line, dst_end_col = offset_to_line_col(int(dst_end), line_offsets_b)

        # Skip excessively large matches (like entire functions)
        if (src_end_line - src_start_line > 6) or (dst_end_line - dst_start_line > 6):
            continue

        matches_mapping.append({
            "src_start": (src_start_line, src_start_col),
            "src_end": (src_end_line, src_end_col),
            "dst_start": (dst_start_line, dst_start_col),
            "dst_end": (dst_end_line, dst_end_col)
        })

    # sort the matches based on the source start line (total order, see map_changes_to_lines)
    matches_mapping.sort(key=lambda x: (x["src_start"][0], x["src_start"][1], x["src_end"][0], x["src_end"][1],
                                        x["dst_start"][0], x["dst_start"][1], x["dst_end"][0], x["dst_end"][1]))

    return matches_mapping