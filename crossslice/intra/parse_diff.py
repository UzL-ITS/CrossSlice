import re
import os
import sys
import numpy as np

# Add the project root to Python path

from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC
from crossslice.intra.ts_utils.source_code_parser_java import SourceCodeParserJava
from crossslice.intra.general_code_analyzer import filter_function_definitions_tree, intersects_with_changes, ast_to_code

C_TYPE_SEPCIFIERS = [
    "struct_specifier",
    "union_specifier",
    "enum_specifier",
    "macro_type_specifier",
    "sized_type_specifier",
    "primitive_type",
    "_type_identifier",
]

C_CPP_EXTENSIONS = (".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx")

def get_relative_path(file_path, root_dir):
    """
    Get the relative path of a file from a root directory
    """
    return os.path.relpath(file_path, root_dir)

def path_to_identifier(relative_path: str) -> str:
    # Replace OS path separators and dots with underscores
    return re.sub(r'[\/\\\.]', '_', relative_path.strip())

def sanitize_filename(function_name: str) -> str:
    # Replace whitespace with underscores
    name_with_underscores = re.sub(r'\s+', '_', function_name)
    # Remove invalid characters (keep letters, numbers, underscores)
    sanitized = re.sub(r'[^\w]', '', name_with_underscores)
    return sanitized

def create_parser(file_path: str):
    """
    Create the appropriate parser based on file extension.
    """
    if file_path == "/dev/null" or not file_path:
        return None
    
    if file_path.endswith(".java"):
        return SourceCodeParserJava(file_path)
    elif file_path.endswith(C_CPP_EXTENSIONS):
        return SourceCodeParserC(file_path)
    else:
        return None
    
def get_context_for_line(parser, line_number):
    """
    Get context for a line number using hierarchical priority:
    1. Function/method context (highest priority)
    2. Class/struct context (if not in function but in class/struct)
    3. Global context (if not in function and not in class/struct)
    """
    if hasattr(parser, 'get_hierarchical_context_for_line'):
        # Both Java and C parsers with proper hierarchical context
        return parser.get_hierarchical_context_for_line(line_number)
    else:
        # Fallback for parsers without hierarchical context
        function_info = parser.get_function_info(line_number)
        if function_info:
            return {
                'type': 'function',
                'name': function_info['name_raw'],
                'full_context': function_info['name_raw'],
                'function': function_info
            }
        else:
            return {
                'type': '__global_context__',
                'name': '__global_context__',
                'full_context': '__global_context__',
                'function': None
            }
        
def extract_function_signature(parser, context_info):
    """
    Extract a more detailed function signature for better matching.
    Works with both context objects and function info objects.
    """
    try:
        # Check if it's a context object or function info object
        if 'function' in context_info and context_info['function']:
            # It's a context object with function info
            fn_info = context_info['function']
        elif 'node' in context_info:
            # It's a function info object
            fn_info = context_info
        else:
            # No function node available (e.g., global context)
            return context_info.get('name', context_info.get('full_context', ''))
        
        # Get the full function signature including return type and parameters
        node = fn_info['node']
        signature = parser.get_text_from_node(node).split('{')[0].strip()
        
        # Extract just the declaration part (before the opening brace)
        if '{' in signature:
            signature = signature.split('{')[0].strip()
        
        return signature
    except Exception:
        # Fallback to basic name if extraction fails
        return context_info.get('name', context_info.get('full_context', ''))
    
def hungarian_matching(old_functions, new_functions, similarity_threshold=0.6):
    """
    Use Hungarian algorithm for optimal function matching when available.
    Falls back to greedy approach if scipy is not available.
    """
    try:
        from scipy.optimize import linear_sum_assignment
        import numpy as np
        
        old_keys = list(old_functions.keys())
        new_keys = list(new_functions.keys())
        
        if not old_keys or not new_keys:
            return {}
        
        # Create cost matrix (convert similarity to cost)
        cost_matrix = np.zeros((len(old_keys), len(new_keys)))
        
        for i, old_key in enumerate(old_keys):
            for j, new_key in enumerate(new_keys):
                similarity = function_similarity_score(old_functions[old_key], new_functions[new_key])
                cost_matrix[i, j] = 1.0 - similarity  # Convert to cost
        
        # Apply Hungarian algorithm
        old_indices, new_indices = linear_sum_assignment(cost_matrix)
        
        # Extract matches above threshold
        matches = {}
        for old_idx, new_idx in zip(old_indices, new_indices):
            similarity = 1.0 - cost_matrix[old_idx, new_idx]
            if similarity >= similarity_threshold:
                matches[old_keys[old_idx]] = new_keys[new_idx]
        
        return matches
        
    except ImportError:
        # Fall back to greedy approach if scipy is not available
        return find_best_function_matches(old_functions, new_functions, similarity_threshold)
    
def function_similarity_score(func1_info, func2_info, position_weight=0.3):
    """
    Calculate comprehensive similarity between two functions.
    Returns a score from 0.0 to 1.0.
    """
    # Extract function information
    name1 = func1_info.get('name_raw', '')
    name2 = func2_info.get('name_raw', '')
    sig1 = func1_info.get('signature', func1_info.get('name', ''))
    sig2 = func2_info.get('signature', func2_info.get('name', ''))
    pos1 = func1_info.get('start_line', 0)
    pos2 = func2_info.get('start_line', 0)
    
    # 1. Exact name match gets highest priority
    if name1 == name2:
        return 1.0
    
    # 2. Check if functions should be merged based on naming patterns
    if should_merge_functions(name1, name2):
        return 0.95
    
    # 3. Name similarity using Levenshtein distance
    max_name_len = max(len(name1), len(name2))
    if max_name_len == 0:
        name_similarity = 0.0
    else:
        name_distance = levenshtein_distance(name1, name2)
        name_similarity = 1.0 - (name_distance / max_name_len)
    
    # 4. Signature similarity
    norm_sig1 = normalize_function_signature(sig1)
    norm_sig2 = normalize_function_signature(sig2)
    max_sig_len = max(len(norm_sig1), len(norm_sig2))
    if max_sig_len == 0:
        sig_similarity = 0.0
    else:
        sig_distance = levenshtein_distance(norm_sig1, norm_sig2)
        sig_similarity = 1.0 - (sig_distance / max_sig_len)
    
    # 5. Position proximity (functions close to each other are more likely to be the same)
    max_file_lines = 10000  # Assume reasonable file size for normalization
    position_distance = abs(pos1 - pos2)
    position_similarity = max(0.0, 1.0 - (position_distance / max_file_lines))
    
    # 6. Special handling for common function name patterns
    # Strip common prefixes/suffixes that might change
    stripped_name1 = re.sub(r'^(old_|new_|_+)', '', name1).rstrip('_')
    stripped_name2 = re.sub(r'^(old_|new_|_+)', '', name2).rstrip('_')
    
    if stripped_name1 == stripped_name2 and stripped_name1:
        name_similarity = max(name_similarity, 0.9)
    
    # 7. Check for substring matches (one function name contains the other)
    if name1 and name2:
        if name1 in name2 or name2 in name1:
            length_ratio = min(len(name1), len(name2)) / max(len(name1), len(name2))
            name_similarity = max(name_similarity, 0.7 * length_ratio)
    
    # Weighted combination of similarities
    combined_score = (
        name_similarity * 0.5 +           # Name is most important
        sig_similarity * 0.3 +            # Signature is second
        position_similarity * position_weight  # Position helps break ties
    )
    
    return min(1.0, combined_score)

def normalize_function_signature(signature):
    """Normalize function signature for comparison."""
    # Remove extra whitespace and normalize spacing
    normalized = re.sub(r'\s+', ' ', signature.strip())
    # Remove parameter names, keeping only types
    normalized = re.sub(r'\b[a-zA-Z_][a-zA-Z0-9_]*\s*(?=[,)])', '', normalized)
    return normalized


def levenshtein_distance(s1, s2):
    """Calculate the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def should_merge_functions(func1_name, func2_name):
    """
    Determine if two function names likely refer to the same function
    based on common naming patterns in version control.
    """
    # Remove common version-control related prefixes/suffixes
    patterns_to_remove = [
        r'^old_', r'^new_', r'^tmp_', r'^temp_',
        r'_old$', r'_new$', r'_tmp$', r'_temp$',
        r'^_+', r'_+$'  # leading/trailing underscores
    ]
    
    clean_name1 = func1_name
    clean_name2 = func2_name
    
    for pattern in patterns_to_remove:
        clean_name1 = re.sub(pattern, '', clean_name1)
        clean_name2 = re.sub(pattern, '', clean_name2)
    
    # If cleaned names are identical, they're likely the same function
    if clean_name1 == clean_name2 and clean_name1:
        return True
    
    # Check for common parameter changes (like type changes)
    # Extract function name without parameters
    base_name1 = clean_name1.split('(')[0] if '(' in clean_name1 else clean_name1
    base_name2 = clean_name2.split('(')[0] if '(' in clean_name2 else clean_name2
    
    return base_name1 == base_name2 and base_name1

def find_best_function_matches(old_functions, new_functions, similarity_threshold=0.6, debug=False):
    """
    Find the best matches between old and new functions using a more sophisticated algorithm.
    Returns a mapping of old_function_key -> new_function_key.
    """
    matches = {}
    used_new_functions = set()
    
    # Create similarity matrix
    similarity_matrix = []
    old_keys = list(old_functions.keys())
    new_keys = list(new_functions.keys())
    
    for old_key in old_keys:
        old_func = old_functions[old_key]
        similarities = []
        for new_key in new_keys:
            new_func = new_functions[new_key]
            if debug:
                # score = debug_function_similarity(old_func, new_func, old_key, new_key)
                pass
            else:
                score = function_similarity_score(old_func, new_func)
            similarities.append((score, new_key))
        similarity_matrix.append((old_key, similarities))
    
    # Sort by best matches first (greedy approach)
    # First, handle exact matches
    for old_key, similarities in similarity_matrix:
        similarities.sort(reverse=True, key=lambda x: x[0])
        best_score, best_new_key = similarities[0]
        
        if best_score == 1.0 and best_new_key not in used_new_functions:
            matches[old_key] = best_new_key
            used_new_functions.add(best_new_key)
            if debug:
                print(f"  Exact match: {old_key} -> {best_new_key}")
    
    # Then handle remaining functions with threshold
    for old_key, similarities in similarity_matrix:
        if old_key in matches:
            continue
            
        similarities.sort(reverse=True, key=lambda x: x[0])
        for score, new_key in similarities:
            if score >= similarity_threshold and new_key not in used_new_functions:
                matches[old_key] = new_key
                used_new_functions.add(new_key)
                if debug:
                    print(f"  Threshold match: {old_key} -> {new_key} (score: {score:.3f})")
                break
    
    return matches

def process_global_context_diff(raw_diff_lines):
    """
    Process raw git diff lines for global context (outside functions/methods).
    Converts git diff format to our diff format like:
    [MOD] #include [- <stdio.h> -] {+<stdlib.h> +}
    [DEL] #include <math.h>
    [ADD] int z;
    """
    result_lines = []
    
    # Group consecutive lines by type
    i = 0
    while i < len(raw_diff_lines):
        line = raw_diff_lines[i]
        
        if line.startswith('-'):
            # Deletion or modification
            deleted_lines = []
            j = i
            while j < len(raw_diff_lines) and raw_diff_lines[j].startswith('-'):
                deleted_lines.append(raw_diff_lines[j][1:].strip())  # Remove - prefix
                j += 1
            
            # Check if there are corresponding additions
            added_lines = []
            k = j
            while k < len(raw_diff_lines) and raw_diff_lines[k].startswith('+'):
                added_lines.append(raw_diff_lines[k][1:].strip())  # Remove + prefix
                k += 1
            
            # Process the group
            if added_lines:
                # Modification: try to match deleted and added lines
                result_lines.extend(create_modification_diff(deleted_lines, added_lines))
                i = k
            else:
                # Pure deletion
                for del_line in deleted_lines:
                    if del_line.strip() and not del_line.strip().startswith('//'):  # Skip empty and comment lines
                        result_lines.append(f"[DEL] {del_line}")
                i = j
                
        elif line.startswith('+'):
            # Pure addition
            added_lines = []
            j = i
            while j < len(raw_diff_lines) and raw_diff_lines[j].startswith('+'):
                added_line = raw_diff_lines[j][1:].strip()  # Remove + prefix
                if added_line.strip() and not added_line.strip().startswith('//'):  # Skip empty and comment lines
                    added_lines.append(added_line)
                j += 1
            
            for add_line in added_lines:
                result_lines.append(f"[ADD] {add_line}")
            i = j
            
        else:
            # Context line (unchanged), skip
            i += 1
    
    return result_lines

def create_modification_diff(deleted_lines, added_lines):
    """
    Create modification diff by matching deleted and added lines.
    Uses simple word-level matching for now.
    """
    result = []
    
    # Simple approach: pair lines by index if same count, otherwise show as separate del/add
    if len(deleted_lines) == len(added_lines):
        for del_line, add_line in zip(deleted_lines, added_lines):
            if del_line.strip() and add_line.strip():
                # Skip empty and comment lines
                if not del_line.strip().startswith('//') and not add_line.strip().startswith('//'):
                    mod_diff = create_word_level_diff(del_line, add_line)
                    result.append(f"[MOD] {mod_diff}")
    else:
        # Different counts - show as separate deletions and additions
        for del_line in deleted_lines:
            if del_line.strip() and not del_line.strip().startswith('//'):
                result.append(f"[DEL] {del_line}")
        for add_line in added_lines:
            if add_line.strip() and not add_line.strip().startswith('//'):
                result.append(f"[ADD] {add_line}")
    
    return result

def create_word_level_diff(old_line, new_line):
    """
    Create word-level diff between two lines.
    Returns format like: word [- old -] {+ new +} word
    """
    import difflib
    
    old_words = old_line.split()
    new_words = new_line.split()
    
    # Use difflib to find differences
    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    result_parts = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            result_parts.extend(old_words[i1:i2])
        elif tag == 'delete':
            deleted_words = ' '.join(old_words[i1:i2])
            result_parts.append(f"[- {deleted_words} -]")
        elif tag == 'insert':
            inserted_words = ' '.join(new_words[j1:j2])
            result_parts.append(f"{{+ {inserted_words} +}}")
        elif tag == 'replace':
            deleted_words = ' '.join(old_words[i1:i2])
            inserted_words = ' '.join(new_words[j1:j2])
            result_parts.append(f"[- {deleted_words} -]{{+ {inserted_words} +}}")
    
    return ' '.join(result_parts)

def parse_diff(text_diff_out: str, output_dir: str, root_dir_old: str, root_dir_new: str, debug_matching=False, use_hungarian=True):
    function_mapping = {}
    current_file = None
    current_hunk_lines = []  # To capture raw diff lines
    current_hunk_context = None
    file_pat = re.compile(r"^diff --git a/(.*?) b/(.*?)$")
    null_pat = re.compile(r"^--- (/dev/null)$|^\+\+\+ (/dev/null)$")
    hunk_pat = re.compile(r"@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@(.*)")

    for line in text_diff_out.splitlines():
        m = file_pat.match(line)
        if m:
            # Save previous hunk if exists
            if current_file and current_hunk_context and current_hunk_lines:
                if current_hunk_context not in function_mapping[current_file]["functions"]:
                    function_mapping[current_file]["functions"][current_hunk_context] = {
                        "old_lines": [], "new_lines": [], 
                        "old_initial_lines": [None, None], "new_initial_lines": [None, None],
                        "old_mapped_lines": [None, None], "new_mapped_lines": [None, None],
                        "raw_diff_lines": []
                    }
                function_mapping[current_file]["functions"][current_hunk_context]["raw_diff_lines"].extend(current_hunk_lines)
            
            current_hunk_lines = []
            current_hunk_context = None
            
            old_f, new_f = m.group(1), m.group(2)
            # Support both C and Java files
            # if not (old_f.endswith(".c") or old_f.endswith(".h") or old_f.endswith(".java")):
            if not (old_f.endswith(C_CPP_EXTENSIONS) or old_f.endswith(".java")):
            # if not old_f.endswith(".java"):
                current_file = None
                continue

            current_file = new_f
            if current_file not in function_mapping:
                function_mapping[current_file] = {
                    "old_file": old_f,
                    "new_file": new_f,
                    "status": "modified",
                    "functions": {},
                }
            continue

        # detect new or deleted files
        m = null_pat.match(line)
        if m:
            if "---" in line: # Old file doesnt exist
                function_mapping[current_file]["status"] = "added"
                function_mapping[current_file]["old_file"] = "/dev/null"
            elif "+++" in line: # New file doesnt exist
                function_mapping[current_file]["status"] = "deleted"
                function_mapping[current_file]["new_file"] = "/dev/null"
            continue

        if current_file is None:
            continue

        # parse hunk header
        m = hunk_pat.match(line)
        if m:
            # Save previous hunk if exists
            if current_hunk_context and current_hunk_lines:
                if current_hunk_context not in function_mapping[current_file]["functions"]:
                    function_mapping[current_file]["functions"][current_hunk_context] = {
                        "old_lines": [], "new_lines": [],
                        "old_initial_lines": [None, None], "new_initial_lines": [None, None], 
                        "old_mapped_lines": [None, None], "new_mapped_lines": [None, None],
                        "raw_diff_lines": [], "g_ctx_lines_old": [], "g_ctx_lines_new": []
                    }
                function_mapping[current_file]["functions"][current_hunk_context]["raw_diff_lines"].extend(current_hunk_lines)
            
            current_hunk_lines = []
            
            old_start = int(m.group(1)) - 1
            old_count = int(m.group(2) or 1)
            new_start = int(m.group(3)) - 1
            new_count = int(m.group(4) or 1)
            context = m.group(5).strip() or "__global_context__"
            current_hunk_context = context
            funcs = function_mapping[current_file]["functions"] 

            if context not in funcs:
                funcs[context] = {
                    "old_lines": [],
                    "new_lines": [],
                    "old_initial_lines": [None, None],
                    "new_initial_lines": [None, None],
                    "old_mapped_lines": [None, None],
                    "new_mapped_lines": [None, None],
                    "raw_diff_lines": [],
                    "g_ctx_lines_old": [],
                    "g_ctx_lines_new": []
                }

            entry = funcs[context]
            # calculate zero-based ranges
            old_end = old_start + max(old_count - 1, 0)
            new_end = new_start + max(new_count - 1, 0)

            if old_count > 0:
                entry["old_lines"].extend(range(old_start, old_end + 1))
            if new_count > 0:
                entry["new_lines"].extend(range(new_start, new_end + 1))

            # -1 if function was deleted completely or added completely
            if old_count == 0:
                entry["old_temp_line"] = old_start
                entry["g_ctx_lines_old"].append(old_start)
            if new_count == 0:
                entry["new_temp_line"] = new_start
                entry["g_ctx_lines_new"].append(new_start)
            continue
        
        # Capture raw diff lines (-, +, or context lines)
        if current_hunk_context and (line.startswith('-') or line.startswith('+') or line.startswith(' ')):
            current_hunk_lines.append(line)
            continue
    

    # Save last hunk if exists
    if current_file and current_hunk_context and current_hunk_lines:
        if current_hunk_context not in function_mapping[current_file]["functions"]:
            function_mapping[current_file]["functions"][current_hunk_context] = {
                "old_lines": [], "new_lines": [],
                "old_initial_lines": [None, None], "new_initial_lines": [None, None],
                "old_mapped_lines": [None, None], "new_mapped_lines": [None, None], 
                "raw_diff_lines": []
            }
        function_mapping[current_file]["functions"][current_hunk_context]["raw_diff_lines"].extend(current_hunk_lines)

    # print(function_mapping)
    # return

    # return function_mapping
    # Now extract full functions spans and write out code
    for rel, info in function_mapping.items():
        old_path = info["old_file"] if info["old_file"] else None
        new_path = info["new_file"] if info["new_file"] else None

        parser_old = create_parser(f"/{old_path}") if old_path != "/dev/null" else None
        parser_new = create_parser(f"/{new_path}") if new_path != "/dev/null" else None

        # Collect all functions from both old and new files
        old_functions = {}  # function_name -> function_info
        new_functions = {}  # function_name -> function_info
        
        for function in info["functions"]:
            entry = info["functions"][function]
            old_lines = entry["old_lines"]
            new_lines = entry["new_lines"]
            old_temp_line = entry.get("old_temp_line", None)
            new_temp_line = entry.get("new_temp_line", None)

            if not old_lines and not new_lines:
                continue

            context_name_old = ""
            context_name_new = ""

            # Process old file functions using hierarchical context
            if parser_old and old_lines:
                for line in old_lines:
                    # print(line)
                    context = get_context_for_line(parser_old, line)
                    if not context:
                        continue

                    # Use hierarchical context name (function -> class -> global)
                    context_name = context['full_context']
                    context_name_old = context_name
                    
                    # Extract function info to maintain expected structure
                    if context.get('function'):
                        # Function context: use the nested function info
                        base_info = context['function']
                    else:
                        # Class or global context: create minimal info structure
                        base_info = {
                            'name': context['name'],
                            'name_raw': context['name'],
                            'start_line': context['class']['start_line'] if context.get('class') else 0, 
                            'end_line': context['class']['end_line'] if context.get('class') else 0,
                            'node': None
                        }
                    
                    # Create enhanced function info with signature
                    signature = extract_function_signature(parser_old, context)
                    # print(f"Extracted signature: {signature}")
                    lines_context = old_functions.get(context_name, {}).get('lines', [])
                    # lines = old_lines if old_lines == [] or old_lines is None else np.unique(np.concatenate((lines_context, [line]))).astype(int).tolist()
                    lines = np.unique(np.concatenate((lines_context, [line]))).astype(int).tolist()
                    # check if g_ctx_lines exist and is not ecmpty array, then concat it
                    if entry.get("g_ctx_lines_old", None) is not None and entry["g_ctx_lines_old"]:
                        lines = np.unique(np.concatenate((lines, entry["g_ctx_lines_old"]))).astype(int).tolist()
                    enhanced_info = {
                        **base_info,
                        'signature': signature,
                        'lines': lines,
                        'temp_line': old_temp_line,
                        'context_type': context['type'],
                        'full_context': context['full_context']
                    }
                    old_functions[context_name] = enhanced_info

                # if function == "FILE                        *AcpiGbl_OutputFile;":
                #     print(f"Debugging function: {function}")
                #     print(f"context: {context}")


            elif parser_old and not old_lines and entry.get("old_temp_line", None) is not None:
                temp_line = entry["old_temp_line"]
                if temp_line >= 0:
                    context = get_context_for_line(parser_old, temp_line)
                    # print("#" * 50)
                    # print(f"Processing old temp line {temp_line} in function {function}: context={context}")
                    if context:
                        context_name = context['full_context']
                        context_name_old = context_name
                        
                        # Extract function info to maintain expected structure
                        if context.get('function'):
                            base_info = context['function']
                        else:
                            base_info = {
                                'name': context['name'],
                                'name_raw': context['name'],
                                'start_line': context['class']['start_line'] if context.get('class') else 0,
                                'end_line': context['class']['end_line'] if context.get('class') else 0,
                                'node': None
                            }
                        
                        signature = extract_function_signature(parser_old, context)
                        # print(f"Extracted signature: {signature}")
                        lines_context = old_functions.get(context_name, {}).get('lines', [])
                        lines = np.unique(np.concatenate((lines_context, [temp_line]))).astype(int).tolist()
                        # check if g_ctx_lines exist and is not ecmpty array, then concat it
                        if entry.get("g_ctx_lines_old", None) is not None and entry["g_ctx_lines_old"]:
                            lines = np.unique(np.concatenate((lines, entry["g_ctx_lines_old"]))).astype(int).tolist()
                        enhanced_info = {
                            **base_info,
                            'signature': signature,
                            'lines': lines,
                            'temp_line': old_temp_line,
                            'context_type': context['type'],
                            'full_context': context['full_context']
                        }
                        old_functions[context_name] = enhanced_info

            # Process new file functions using hierarchical context
            if parser_new and new_lines:
                for line in new_lines:
                    context = get_context_for_line(parser_new, line)
                    # print("#" * 50)
                    # print(f"Processing new line {line} in function {function}: context={context}")
                    if not context:
                        continue

                    # Use hierarchical context name (function -> class -> global)
                    context_name = context['full_context']
                    context_name_new = context_name
                    
                    # Extract function info to maintain expected structure
                    if context.get('function'):
                        # Function context: use the nested function info
                        base_info = context['function']
                    else:
                        # Class or global context: create minimal info structure
                        base_info = {
                            'name': context['name'],
                            'name_raw': context['name'],
                            'start_line': context['class']['start_line'] if context.get('class') else 0,
                            'end_line': context['class']['end_line'] if context.get('class') else 0,
                            'node': None
                        }
                    
                    # Create enhanced function info with signature
                    signature = extract_function_signature(parser_new, context)
                    # print(f"Extracted signature: {signature}")
                    lines_context = new_functions.get(context_name, {}).get('lines', [])
                    # lines = new_lines if new_lines == [] or new_lines is None else np.unique(np.concatenate((lines_context, [line]))).astype(int).tolist()
                    lines = np.unique(np.concatenate((lines_context, [line]))).astype(int).tolist()
                    # check if g_ctx_lines exist and is not ecmpty array, then concat it
                    if entry.get("g_ctx_lines_new", None) is not None and entry["g_ctx_lines_new"]:
                        lines = np.unique(np.concatenate((lines, entry["g_ctx_lines_new"]))).astype(int).tolist()

                    enhanced_info = {
                        **base_info,
                        'signature': signature,
                        'lines': lines,
                        'temp_line': new_temp_line,
                        'context_type': context['type'],
                        'full_context': context['full_context']
                    }
                    new_functions[context_name] = enhanced_info
            elif parser_new and not new_lines and entry.get("new_temp_line", None) is not None:
                temp_line = entry["new_temp_line"]
                if temp_line >= 0:
                    context = get_context_for_line(parser_new, temp_line)
                    # print("#" * 50)
                    # print(f"Processing new temp line {temp_line} in function {function}: context={context}")
                    if context:
                        context_name = context['full_context']
                        context_name_new = context_name
                        
                        # Extract function info to maintain expected structure
                        if context.get('function'):
                            base_info = context['function']
                        else:
                            base_info = {
                                'name': context['name'],
                                'name_raw': context['name'],
                                'start_line': context['class']['start_line'] if context.get('class') else 0,
                                'end_line': context['class']['end_line'] if context.get('class') else 0,
                                'node': None
                            }
                        
                        signature = extract_function_signature(parser_new, context)
                        # print(f"Extracted signature: {signature}")
                        lines_context = new_functions.get(context_name, {}).get('lines', [])
                        lines = np.unique(np.concatenate((lines_context, [temp_line]))).astype(int).tolist()
                        # check if g_ctx_lines exist and is not ecmpty array, then concat it
                        if entry.get("g_ctx_lines_new", None) is not None and entry["g_ctx_lines_new"]:
                            lines = np.unique(np.concatenate((lines, entry["g_ctx_lines_new"]))).astype(int).tolist()
                        enhanced_info = {
                            **base_info,
                            'signature': signature,
                            'lines': lines,
                            'temp_line': new_temp_line,
                            'context_type': context['type'],
                            'full_context': context['full_context']
                        }
                        new_functions[context_name] = enhanced_info

            if parser_new and parser_old:
                lines_old = old_functions.get(context_name_old, {}).get('lines', [])
                lines_new = new_functions.get(context_name_new, {}).get('lines', [])

                g_ctx_old = entry.get("g_ctx_lines_old", [])
                g_ctx_new = entry.get("g_ctx_lines_new", [])

                lines_old = np.unique(np.concatenate((lines_old, g_ctx_old))).astype(int).tolist()
                lines_new = np.unique(np.concatenate((lines_new, g_ctx_new))).astype(int).tolist()

                # Update the function info with the lines
                old_functions[context_name_old]['lines'] = lines_old
                new_functions[context_name_new]['lines'] = lines_new

        # Filter lines to ensure each function only gets lines within its boundaries
        if rel.endswith('.java'):
            pass
            # old_functions = filter_function_lines_java(old_functions)
            # new_functions = filter_function_lines_java(new_functions)
            
            # # Find missing functions that exist in source files but weren't captured in diff
            # old_functions, new_functions = find_missing_functions_java(old_functions, new_functions, parser_old, parser_new)
        
        # Now find the best matches between old and new functions
        # print(f"Old functions for {rel}: {old_functions}")
        # print(f"New functions for {rel}: {new_functions}")
        if use_hungarian:
            function_matches = hungarian_matching(old_functions, new_functions)
        else:
            function_matches = find_best_function_matches(old_functions, new_functions, debug=debug_matching)

        # print("" + "=" * 50)
        # print(f"Function matches for {rel}: {function_matches}")
        
        # Debug output
        if debug_matching:
            print(f"File: {rel}")
            print(f"Old functions: {list(old_functions.keys())}")
            print(f"New functions: {list(new_functions.keys())}")
            print(f"Matches found: {function_matches}")
            print("---")
        
        # Create the final function mapping
        final_functions = {}
        
        # Add matched pairs
        for old_name, new_name in function_matches.items():
            old_func = old_functions[old_name]
            new_func = new_functions[new_name]
            
            # Find the original entry to get raw_diff_lines
            original_entry = None
            for context_name, context_data in info["functions"].items():
                if context_name == old_name or context_name == new_name:
                    original_entry = context_data
                    break
            
            # Use old function name as key, but could also use a combined key
            final_functions[old_name] = {
                "old_lines": old_func.get('lines', []),
                "new_lines": new_func.get('lines', []),
                "old_initial_lines": [old_func["start_line"], old_func["end_line"]],
                "new_initial_lines": [new_func["start_line"], new_func["end_line"]],
                "old_file_path": None, "new_file_path": None,
                "old_code": None, "new_code": None,
                "old_temp_line": old_func.get('temp_line'),
                "new_temp_line": new_func.get('temp_line'),
                "context_type": old_func.get('context_type', new_func.get('context_type', 'unknown')),
                "full_context": old_func.get('full_context', new_func.get('full_context', old_name)),
                "raw_diff_lines": original_entry.get('raw_diff_lines', []) if original_entry else []
            }
        
        # Add unmatched old functions (deletions)
        for old_name, old_func in old_functions.items():
            if old_name not in function_matches:
                # Find the original entry to get raw_diff_lines
                original_entry = None
                for context_name, context_data in info["functions"].items():
                    if context_name == old_name:
                        original_entry = context_data
                        break
                        
                final_functions[old_name] = {
                    "old_lines": old_func.get('lines', []),
                    "new_lines": [],
                    "old_initial_lines": [old_func["start_line"], old_func["end_line"]],
                    "new_initial_lines": [None, None],
                    "old_file_path": None, "new_file_path": None,
                    "old_code": None, "new_code": None,
                    "old_temp_line": old_func.get('temp_line'),
                    "new_temp_line": None,
                    "context_type": old_func.get('context_type', 'unknown'),
                    "full_context": old_func.get('full_context', old_name),
                    "raw_diff_lines": original_entry.get('raw_diff_lines', []) if original_entry else []
                }
        
        # Add unmatched new functions (additions)
        matched_new_names = set(function_matches.values())
        for new_name, new_func in new_functions.items():
            if new_name not in matched_new_names:
                # Find the original entry to get raw_diff_lines
                original_entry = None
                for context_name, context_data in info["functions"].items():
                    if context_name == new_name:
                        original_entry = context_data
                        break
                        
                final_functions[new_name] = {
                    "old_lines": [],
                    "new_lines": new_func.get('lines', []),
                    "old_initial_lines": [None, None],
                    "new_initial_lines": [new_func["start_line"], new_func["end_line"]],
                    "old_file_path": None, "new_file_path": None,
                    "old_code": None, "new_code": None,
                    "old_temp_line": None,
                    "new_temp_line": new_func.get('temp_line'),
                    "context_type": new_func.get('context_type', 'unknown'),
                    "full_context": new_func.get('full_context', new_name),
                    "raw_diff_lines": original_entry.get('raw_diff_lines', []) if original_entry else []
                }

        # Update the function mapping with the final functions
        function_mapping[rel]["functions"] = final_functions
        
        # Process global context diffs directly from raw diff lines
        for func_name, func_data in function_mapping[rel]["functions"].items():
            if func_name == "__global_context__" and "raw_diff_lines" in func_data:
                global_diff = process_global_context_diff(func_data["raw_diff_lines"])
                func_data["global_context_diff"] = global_diff
                if debug_matching:
                    print(f"Global context diff for {rel}:")
                    for diff_line in global_diff:
                        print(f"  {diff_line}")
                    print("---")

    # return function_mapping

    # Now we have the function mapping with all functions and their lines
    for rel, info in function_mapping.items():
        old_path = info["old_file"] if info["old_file"] else None
        new_path = info["new_file"] if info["new_file"] else None

        parser_old = create_parser(f"/{old_path}") if old_path != "/dev/null" else None
        parser_new = create_parser(f"/{new_path}") if new_path != "/dev/null" else None

        source_bytes_old = parser_old.get_source_bytes() if parser_old else None
        source_bytes_new = parser_new.get_source_bytes() if parser_new else None

        rel_old = get_relative_path(f"/{old_path}", root_dir_old) if old_path != "/dev/null" else None
        rel_new = get_relative_path(f"/{new_path}", root_dir_new) if new_path != "/dev/null" else None

        #
        # ────────────────────────────────────────────────────────────────────────────────
        #  Handle global context
        # ────────────────────────────────────────────────────────────────────────────────
        #
        g_ctx_func = info["functions"].get("__global_context__")
        if g_ctx_func:
            # Process global context function
            old_lines = g_ctx_func.get("old_lines", [])
            new_lines = g_ctx_func.get("new_lines", [])

            rel_nodes_old = filter_function_definitions_tree(parser_old.get_top_level_node()) if parser_old else []
            rel_nodes_new = filter_function_definitions_tree(parser_new.get_top_level_node()) if parser_new else []

            rel_nodes_old = [child for child in rel_nodes_old if intersects_with_changes(child, old_lines)] # node instead of child before
            rel_nodes_new = [child for child in rel_nodes_new if intersects_with_changes(child, new_lines)]

            if rel_nodes_old:
                old_code = ""
                for node in rel_nodes_old:
                    # old_code += parser_old.get_function_source_code(node)
                    old_code += ast_to_code(node, source_bytes_old)
                    if node.type in C_TYPE_SEPCIFIERS and not old_code.endswith(";") and not old_code.endswith("\n"):
                        old_code += ";"
                    old_code += "\n"

                filename = f"global_context.c"

                g_ctx_func["old_code"] = old_code
                g_ctx_func["old_file_path"] = os.path.join(output_dir, "functions_code", path_to_identifier(rel_old), "old", filename)
                os.makedirs(os.path.dirname(g_ctx_func["old_file_path"]), exist_ok=True)
                with open(g_ctx_func["old_file_path"], "w") as f:
                    f.write(old_code)

            if rel_nodes_new:
                new_code = ""
                for node in rel_nodes_new:
                    # new_code += parser_new.get_function_source_code(node)
                    new_code += ast_to_code(node, source_bytes_new)
                    if node.type in C_TYPE_SEPCIFIERS and not new_code.endswith(";") and not new_code.endswith("\n"):
                        new_code += ";"
                    new_code += "\n"

                filename = f"global_context.c"

                g_ctx_func["new_code"] = new_code
                g_ctx_func["new_file_path"] = os.path.join(output_dir, "functions_code", path_to_identifier(rel_new), "new", filename)
                os.makedirs(os.path.dirname(g_ctx_func["new_file_path"]), exist_ok=True)
                with open(g_ctx_func["new_file_path"], "w") as f:
                    f.write(new_code)

        for fn_name, data in info["functions"].items():
            if fn_name == "__global_context__":
                continue
            # print(f"Processing old function {fn_name}. Is parser_old: {parser_old is not None}, Is parser_new: {parser_new is not None}. Is old_initial_lines: {data['old_initial_lines']}, Is new_initial_lines: {data['new_initial_lines']}")
            
            # Determine file extension based on the original file
            if rel_old and rel_old.endswith(".java"):
                file_ext = ".java"
            elif rel_old:
                file_ext = os.path.splitext(rel_old)[1] or ".c"
            else:
                file_ext = ".c"
            
            if parser_old and data["old_initial_lines"][0] is not None:
                # print(f"Processing old function {fn_name}. Is parser_old: {parser_old is not None}. Is old_initial_lines: {data['old_initial_lines']}")
                fn_info = parser_old.get_function_info(data["old_initial_lines"][0])
                if not fn_info:
                    continue

                fn_code = parser_old.get_function_source_code(fn_info["node"])
                
                # Determine filename and extension based on context type
                context_type = data.get("context_type", "unknown")
                if context_type == "class":
                    filename = f"{sanitize_filename(fn_info['name_raw'])}_class{file_ext}"
                else:
                    filename = f"{sanitize_filename(fn_info['name_raw'])}{file_ext}"
                
                fn_file_path = os.path.join(output_dir, "functions_code", path_to_identifier(rel_old), "old", filename)
                os.makedirs(os.path.dirname(fn_file_path), exist_ok=True)
                with open(fn_file_path, "w") as f:
                    f.write(fn_code)

                data["old_file_path"] = fn_file_path
                data["old_code"] = fn_code

                # add mapped lines here: range from 0 to length of function code
                data["old_mapped_lines"] = [0, fn_info["end_line"] - fn_info["start_line"] + 1]

            if parser_new and data["new_initial_lines"][0] is not None:
                fn_info = parser_new.get_function_info(data["new_initial_lines"][0])
                if not fn_info:
                    continue

                fn_code = parser_new.get_function_source_code(fn_info["node"])
                
                # Determine filename and extension based on context type
                context_type = data.get("context_type", "unknown")
                if context_type == "class":
                    filename = f"{sanitize_filename(fn_info['name_raw'])}_class{file_ext}"
                else:
                    filename = f"{sanitize_filename(fn_info['name_raw'])}{file_ext}"
                
                fn_file_path = os.path.join(output_dir, "functions_code", path_to_identifier(rel_new), "new", filename)
                os.makedirs(os.path.dirname(fn_file_path), exist_ok=True)
                with open(fn_file_path, "w") as f:
                    f.write(fn_code)

                data["new_file_path"] = fn_file_path
                data["new_code"] = fn_code

                # add mapped lines here: range from 0 to length of function code
                data["new_mapped_lines"] = [0, fn_info["end_line"] - fn_info["start_line"] + 1]

    return function_mapping