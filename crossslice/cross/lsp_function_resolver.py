import json
import sys
import os
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set, Tuple, Any

# Add project root to path

from crossslice.cross.py_clangd_bridge import CompileDBBuilder, ClangdSession
from crossslice.cross.gtags_handler import GtagsHandler

# Standard library functions that we shouldn't try to analyze in detail
STANDARD_LIB_FUNCTIONS = {
    # Memory management
    'malloc', 'calloc', 'realloc', 'free', 'memcpy', 'memset', 'memmove', 'memcmp',
    # String functions  
    'strlen', 'strcpy', 'strncpy', 'strcat', 'strncat', 'strcmp', 'strncmp', 'strchr', 'strstr', 'strtok',
    # I/O functions
    'printf', 'fprintf', 'sprintf', 'snprintf', 'scanf', 'fscanf', 'sscanf', 'fopen', 'fclose', 'fread', 'fwrite',
    'fseek', 'ftell', 'rewind', 'fgetc', 'fgets', 'fputc', 'fputs', 'getchar', 'putchar', 'puts',
    # Math functions
    'abs', 'fabs', 'sqrt', 'pow', 'exp', 'log', 'sin', 'cos', 'tan', 'floor', 'ceil', 'round',
    # Utility functions
    'exit', 'abort', 'atexit', 'system', 'getenv', 'qsort', 'bsearch', 'rand', 'srand', 'time',
    # Character functions
    'isalpha', 'isdigit', 'isalnum', 'isspace', 'tolower', 'toupper',
    # POSIX functions commonly used
    'open', 'close', 'read', 'write', 'lseek', 'stat', 'fstat', 'mkdir', 'rmdir', 'unlink',
}


@dataclass
class FunctionDefinition:
    """Represents a resolved function definition"""
    function_name: str
    file_path: str
    line_number: int  # 0-based
    column: int = 0  # 0-based
    signature: str = ""
    argument_count: int = 0
    is_macro: bool = False
    code_context: str = ""


@dataclass
class LSPResolutionResult:
    """Results from LSP-based function resolution"""
    function_name: str
    gtags_candidates: List[Dict]
    filtered_candidates: List[Dict]  # After argument count filtering
    lsp_definition: Optional[FunctionDefinition]
    resolution_status: str  # "success", "no_candidates", "lsp_failed", "multiple_matches", "standard_lib", "lsp_fallback"
    resolution_method: str = ""  # "lsp", "gtags_fallback", "standard_lib", "first_candidate"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'function_name': self.function_name,
            'gtags_candidates': self.gtags_candidates,
            'filtered_candidates': self.filtered_candidates,
            'lsp_definition': asdict(self.lsp_definition) if self.lsp_definition else None,
            'resolution_status': self.resolution_status,
            'resolution_method': self.resolution_method
        }


@dataclass
class FinalFunctionTarget:
    """Final target for tree-sitter extraction"""
    function_name: str
    file_path: str
    line_number: int  # 0-based
    column: int = 0
    is_macro: bool = False
    signature: str = ""
    argument_count: int = 0
    resolution_method: str = ""  # How this was resolved


class LSPFunctionResolver:
    """Resolves function definitions using LSP after gtags filtering"""

    def __init__(self, repo_dir: str, original_file: str = None):
        self.repo_dir = Path(repo_dir).resolve()
        self.original_file = Path(original_file).resolve() if original_file else None
        self.compile_db_path = None
        self.clangd_session = None

    def _count_macro_arguments(self, code_line: str) -> int:
        """Count arguments in a macro definition"""
        # Look for #define MACRO_NAME(arg1, arg2, ...)
        match = re.search(r'#define\s+\w+\s*\(([^)]*)\)', code_line)
        if not match:
            return 0
        
        args_str = match.group(1).strip()
        if not args_str:
            return 0
        
        # Simple argument counting (split by comma, but be careful of nested parentheses)
        args = [arg.strip() for arg in args_str.split(',')]
        return len([arg for arg in args if arg])

    def _count_function_arguments(self, code_line: str) -> int:
        """Count arguments in a function declaration/definition"""
        # Look for function signature patterns
        # This is a simplified version - might need refinement for complex cases
        
        # Find the parameter list in parentheses
        paren_match = re.search(r'\(([^)]*)\)', code_line)
        if not paren_match:
            return 0
        
        params_str = paren_match.group(1).strip()
        if not params_str or params_str == 'void':
            return 0
        
        # Simple parameter counting
        # Split by comma but be careful of function pointers and nested structures
        params = []
        paren_depth = 0
        current_param = ""
        
        for char in params_str:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == ',' and paren_depth == 0:
                params.append(current_param.strip())
                current_param = ""
                continue
            current_param += char
        
        if current_param.strip():
            params.append(current_param.strip())
        
        return len(params)

    def _calculate_file_priority(self, file_path: str) -> int:
        """
        Calculate priority score for a file path (higher = better)
        
        Priority rules:
        1. Avoid test files/directories (test, tests, Testing, check, etc.)
        2. Prefer main source directories (src, lib, include)
        3. Prefer project files over system/external files
        4. Prefer .h/.c files over other extensions
        """
        path_lower = file_path.lower()
        path_parts = Path(file_path).parts
        
        score = 100  # Base score
        
        # Penalize test-related paths
        test_indicators = ['test', 'tests', 'testing', 'check', 'mock', 'fixture', 'sample', 'example', 'demo']
        for indicator in test_indicators:
            if any(indicator in part.lower() for part in path_parts):
                score -= 50
                break
        
        # Prefer main source directories
        preferred_dirs = ['src', 'source', 'lib', 'libav', 'include', 'inc', 'core', 'main']
        for preferred in preferred_dirs:
            if any(preferred in part.lower() for part in path_parts):
                score += 20
                break
        
        # Prefer project files (containing the project name or in main directories)
        if any(part in ['libavcodec', 'libavutil', 'libavformat'] for part in path_parts):
            score += 15
        
        # File extension preferences
        if file_path.endswith(('.h', '.c')):
            score += 10
        elif file_path.endswith(('.hpp', '.cpp', '.cc')):
            score += 5
        
        # Penalize deeply nested paths (likely generated/vendor code)
        if len(path_parts) > 8:
            score -= 10
        
        return score

    def _filter_candidates_by_argument_count(self, candidates: List[Dict], expected_arg_count: int) -> List[Dict]:
        """Filter and prioritize gtags candidates by argument count and file quality"""
        filtered = []
        
        for candidate in candidates:
            code_line = candidate.get('code_line', '')
            file_path = candidate.get('file_path', '')
            
            # Check if it's a macro
            if code_line.strip().startswith('#define'):
                arg_count = self._count_macro_arguments(code_line)
                candidate['is_macro'] = True
            else:
                arg_count = self._count_function_arguments(code_line)
                candidate['is_macro'] = False
            
            candidate['detected_arg_count'] = arg_count
            candidate['file_priority'] = self._calculate_file_priority(file_path)
            
            if arg_count == expected_arg_count:
                filtered.append(candidate)
        
        # Sort by file priority (highest first) and then by line number for stability
        filtered.sort(key=lambda x: (-x['file_priority'], x.get('line_number', 0)))
        
        return filtered

    def _setup_compile_db_and_lsp(self, target_files: List[str]) -> bool:
        """Setup compile database and LSP session"""
        try:
            # Build compile database for target files
            builder = CompileDBBuilder(self.repo_dir)
            self.compile_db_path = builder.ensure_compile_commands(target_files=target_files)
            

            
            # Initialize clangd session
            self.clangd_session = ClangdSession(
                project_root=self.repo_dir,
                compile_commands_dir=self.compile_db_path.parent,
                debug=False
            )
            
            # Start the session and wait for initialization
            self.clangd_session.start()
            
            # Open the original file if provided
            if self.original_file and self.original_file.exists():
                self.clangd_session.open(str(self.original_file), language_id="c")
            
            return True
            
        except Exception as e:

            return False

    def _try_lsp_hover_for_macro(self, file_path: str, line_number: int, function_name: str) -> Optional[str]:
        """Try to get macro information via LSP hover"""
        try:
            self.clangd_session.open(str(file_path), language_id="c")
            
            # LSP hover can sometimes provide macro information
            # This is a placeholder - the actual hover method would need to be implemented in the LSP client
            # For now, we'll skip this and rely on gtags for macros
            return None
        except Exception:
            return None

    def _resolve_with_lsp(self, function_name: str, candidates: List[Dict], 
                         call_site_file: str = None, call_site_line: int = None, 
                         call_site_col: int = None) -> Optional[FunctionDefinition]:
        """Use LSP to resolve the exact function definition"""
        if not self.clangd_session:
            return None
        
        try:
            # If we have a call site, use it to get the definition
            if call_site_file and call_site_line is not None and call_site_col is not None:
                # Open the call site file
                call_file_path = Path(call_site_file)
                if call_file_path.exists():
                    self.clangd_session.open(str(call_file_path), language_id="c")
                    
                    # Get definition from call site
                    definition_result = self.clangd_session.definition(
                        file=str(call_file_path),
                        line=call_site_line,  # LSP uses 0-based lines
                        col=call_site_col
                    )
                    
                    if definition_result:
                        # Extract definition information
                        if isinstance(definition_result, list) and len(definition_result) > 0:
                            def_info = definition_result[0]
                        else:
                            def_info = definition_result
                        
                        if 'uri' in def_info and 'range' in def_info:
                            file_uri = def_info['uri']
                            # Convert file:// URI to path
                            file_path = file_uri.replace('file://', '')
                            
                            line_num = def_info['range']['start']['line']
                            col_num = def_info['range']['start']['character']
                            
                            return FunctionDefinition(
                                function_name=function_name,
                                file_path=file_path,
                                line_number=line_num,
                                column=col_num,
                                signature="",  # Could be extracted from LSP hover
                                argument_count=0,  # Could be determined from signature
                                is_macro=False,  # Could be determined from LSP
                                code_context=""
                            )
            
            # Try each candidate (now sorted by priority)
            for candidate in candidates:
                candidate_file = Path(candidate['file_path'])
                if not candidate_file.exists():
                    continue
                
                is_macro = candidate.get('is_macro', False)
                
                try:
                    # Open candidate file
                    self.clangd_session.open(str(candidate_file), language_id="c")
                    
                    # Try to get definition at the candidate line
                    line_num = candidate['line_number'] - 1  # Convert to 0-based
                    
                    if is_macro:
                        # For macros, LSP definition might not work well
                        # Try LSP first, but be ready to fall back to gtags info
                        definition_result = self.clangd_session.definition(
                            file=str(candidate_file),
                            line=line_num,
                            col=0
                        )
                        
                        if definition_result:
                            # LSP successfully resolved the macro
                            return FunctionDefinition(
                                function_name=function_name,
                                file_path=candidate['file_path'],
                                line_number=line_num,
                                column=0,
                                signature=candidate.get('code_line', ''),
                                argument_count=candidate.get('detected_arg_count', 0),
                                is_macro=True,
                                code_context=candidate.get('code_line', '')
                            )
                        else:
                            # LSP failed for macro, but we have good gtags info
                            # Return the highest priority candidate as the best guess

                            # Mark this for method tracking
                            result = FunctionDefinition(
                                function_name=function_name,
                                file_path=candidate['file_path'],
                                line_number=line_num,
                                column=0,
                                signature=candidate.get('code_line', ''),
                                argument_count=candidate.get('detected_arg_count', 0),
                                is_macro=True,
                                code_context=candidate.get('code_line', '')
                            )
                            # Add a flag to track this was gtags fallback
                            result.code_context += " [GTAGS_FALLBACK]"
                            return result
                    else:
                        # Regular function - LSP should work well
                        definition_result = self.clangd_session.definition(
                            file=str(candidate_file),
                            line=line_num,
                            col=0
                        )
                        
                        if definition_result:
                            # LSP successfully resolved the function
                            return FunctionDefinition(
                                function_name=function_name,
                                file_path=candidate['file_path'],
                                line_number=line_num,
                                column=0,
                                signature=candidate.get('code_line', ''),
                                argument_count=candidate.get('detected_arg_count', 0),
                                is_macro=False,
                                code_context=candidate.get('code_line', '')
                            )
                        
                except Exception as e:
                    # Continue to next candidate

                    continue
            
            # If we have candidates but LSP failed for all, return the highest priority one
            if candidates:
                best_candidate = candidates[0]  # Already sorted by priority

                return FunctionDefinition(
                    function_name=function_name,
                    file_path=best_candidate['file_path'],
                    line_number=best_candidate['line_number'] - 1,  # Convert to 0-based
                    column=0,
                    signature=best_candidate.get('code_line', ''),
                    argument_count=best_candidate.get('detected_arg_count', 0),
                    is_macro=best_candidate.get('is_macro', False),
                    code_context=best_candidate.get('code_line', '')
                )
            
            return None
            
        except Exception as e:

            return None

    def resolve_functions(self, gtags_context: Dict[str, Dict], 
                         function_signatures: Dict[str, int],
                         call_site_info: Dict[str, Dict] = None) -> Dict[str, LSPResolutionResult]:
        """
        Resolve function definitions using LSP
        
        Args:
            gtags_context: Results from gtags analysis
            function_signatures: Dict mapping function_name -> expected_arg_count  
            call_site_info: Optional dict with call site information for better resolution
        """
        results = {}
        
        if not gtags_context:
            return results
        
        # Collect all target files for compile DB
        target_files = set()
        if self.original_file:
            target_files.add(str(self.original_file))
        
        for func_name, func_data in gtags_context.items():
            for definition in func_data.get('definitions', []):
                file_path = definition.get('file_path')
                if file_path and Path(file_path).exists():
                    target_files.add(file_path)
        
        # Setup LSP
        if not self._setup_compile_db_and_lsp(sorted(target_files)):

            # Return gtags results without LSP resolution
            for func_name, func_data in gtags_context.items():
                expected_arg_count = function_signatures.get(func_name, -1)
                candidates = func_data.get('definitions', [])
                filtered = self._filter_candidates_by_argument_count(candidates, expected_arg_count) if expected_arg_count >= 0 else candidates
                
                results[func_name] = LSPResolutionResult(
                    function_name=func_name,
                    gtags_candidates=candidates,
                    filtered_candidates=filtered,
                    lsp_definition=None,
                    resolution_status="lsp_failed"
                )
            return results
        
        try:
            # Process each function
            for func_name, func_data in gtags_context.items():
                expected_arg_count = function_signatures.get(func_name, -1)
                candidates = func_data.get('definitions', [])
                
                # Filter by argument count if we have expected count
                if expected_arg_count >= 0:
                    filtered_candidates = self._filter_candidates_by_argument_count(candidates, expected_arg_count)
                else:
                    filtered_candidates = candidates
                
                print(f"Resolving {func_name}: {len(candidates)} candidates -> {len(filtered_candidates)} after filtering")
                
                # Get call site info for this function
                call_info = call_site_info.get(func_name, {}) if call_site_info else {}
                call_site_file = call_info.get('file_path')
                call_site_line = call_info.get('line_number', 0) if call_info.get('line_number') else None  # Convert to 0-based
                call_site_col = call_info.get('column', 0)
                
                # Skip standard library functions early
                if func_name in STANDARD_LIB_FUNCTIONS:
                    results[func_name] = LSPResolutionResult(
                        function_name=func_name,
                        gtags_candidates=candidates,
                        filtered_candidates=[],
                        lsp_definition=None,
                        resolution_status="standard_lib",
                        resolution_method="standard_lib"
                    )
                    continue
                
                # Resolve with LSP
                lsp_definition = None
                status = "no_candidates"
                method = ""
                
                if filtered_candidates:
                    lsp_definition = self._resolve_with_lsp(
                        func_name, 
                        filtered_candidates,
                        call_site_file,
                        call_site_line, 
                        call_site_col
                    )
                    
                    if lsp_definition:
                        status = "success"
                        # Check if it was a gtags fallback
                        if "[GTAGS_FALLBACK]" in lsp_definition.code_context:
                            method = "gtags_fallback"
                            lsp_definition.code_context = lsp_definition.code_context.replace(" [GTAGS_FALLBACK]", "")
                        else:
                            method = "lsp"
                    else:
                        status = "lsp_failed"
                        method = "lsp_failed"
                elif candidates:
                    # Had candidates but none passed argument filtering
                    status = "filtered_out"
                    method = "filtered_out"
                
                results[func_name] = LSPResolutionResult(
                    function_name=func_name,
                    gtags_candidates=candidates,
                    filtered_candidates=filtered_candidates,
                    lsp_definition=lsp_definition,
                    resolution_status=status,
                    resolution_method=method
                )
        
        finally:
            # Cleanup LSP session
            if self.clangd_session:
                self.clangd_session.stop()
                self.clangd_session = None
        
        return results

    def resolve_functions_for_commit(self, repo_dir: str, commit_hash: str,
                                   functions_with_signatures: Dict[str, int],
                                   original_file: str = None) -> Dict[str, LSPResolutionResult]:
        """
        Resolve functions for a specific commit
        
        Args:
            repo_dir: Repository directory
            commit_hash: Git commit hash to checkout
            functions_with_signatures: Dict mapping function_name -> expected_arg_count
            original_file: Original file containing the function calls
        """
        results = {}
        
        try:
            with GtagsHandler(repo_dir) as gtags:
                # Checkout the commit
                if commit_hash and not gtags.checkout_commit(commit_hash):

                    return results
                
                # Generate GTAGS if needed
                if not gtags.check_gtags():

                    gtags.generate_gtags()
                    
                    if not gtags.check_gtags():

                        return results
                
                # Get gtags context for all functions
                gtags_context = {}
                for func_name in functions_with_signatures.keys():
                    func_context = gtags.get_function_context(func_name)
                    if func_context['definitions']:
                        gtags_context[func_name] = func_context
                
                # Setup LSP resolver
                resolver = LSPFunctionResolver(repo_dir, original_file)
                
                # Resolve with LSP
                results = resolver.resolve_functions(
                    gtags_context=gtags_context,
                    function_signatures=functions_with_signatures
                )
        
        except Exception as e:

            import traceback
            traceback.print_exc()
        
        return results
    
    def get_final_targets_for_tree_sitter(self, lsp_results: Dict[str, LSPResolutionResult]) -> List[FinalFunctionTarget]:
        """
        Extract final targets for tree-sitter analysis
        
        Rules:
        1. Skip standard library functions
        2. Use LSP definition if available
        3. Fall back to first filtered candidate if LSP failed
        4. Only one target per function
        """
        targets = []
        
        for func_name, result in lsp_results.items():
            # Skip standard library functions
            if func_name in STANDARD_LIB_FUNCTIONS:
                print(f"Skipping standard library function: {func_name}")
                continue
            
            target = None
            
            if result.lsp_definition:
                # Use LSP definition (preferred)
                lsp_def = result.lsp_definition
                target = FinalFunctionTarget(
                    function_name=func_name,
                    file_path=lsp_def.file_path,
                    line_number=lsp_def.line_number,
                    column=lsp_def.column,
                    is_macro=lsp_def.is_macro,
                    signature=lsp_def.signature,
                    argument_count=lsp_def.argument_count,
                    resolution_method="lsp" if result.resolution_method != "gtags_fallback" else "gtags_fallback"
                )
            elif result.filtered_candidates:
                # Fall back to first (highest priority) filtered candidate
                best_candidate = result.filtered_candidates[0]
                target = FinalFunctionTarget(
                    function_name=func_name,
                    file_path=best_candidate['file_path'],
                    line_number=best_candidate['line_number'] - 1,  # Convert to 0-based
                    column=0,
                    is_macro=best_candidate.get('is_macro', False),
                    signature=best_candidate.get('code_line', ''),
                    argument_count=best_candidate.get('detected_arg_count', 0),
                    resolution_method="first_candidate"
                )
                print(f"Using first filtered candidate for {func_name}: {best_candidate['file_path']}:{best_candidate['line_number']}")
            else:
                print(f"No viable target found for {func_name}")
                continue
            
            if target:
                targets.append(target)
                print(f"Added target for {func_name}: {target.file_path}:{target.line_number} ({target.resolution_method})")
        
        return targets
