"""
This module is used to parse the source code of C language using tree-sitter.
Its based on the SourceCodeParser class that is used to parse the source code of Java and C language.
"""
import re

from .source_code_parser import SourceCodeParser

class SourceCodeParserC(SourceCodeParser):
    
    C_EXTENSIONS = (".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx")

    def __init__(self, file_path: str):
        if not file_path.endswith(self.C_EXTENSIONS):
            raise NotImplementedError("File is not a C/C++ file: " + file_path)
        
        super().__init__(file_path)

    def collect_function_definitions(self) -> list[tuple]:
        """
        Recursively collect function definition nodes from the syntax tree along with their names and start/end lines.

        :return: A list of tuples: (node, start_point, end_point, name, start_line, end_line)
        """

        function_definitions = []

        def collect_function_definitions_rec(node):
            if node.type == "function_definition" or node.type == "method_declaration":
                # Attempt to find the function name node within the function definition
                function_name = self.get_function_name(node)
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                function_definitions.append((node, function_name, start_line, end_line))

            for child in node.children:
                collect_function_definitions_rec(child)

            return function_definitions
        
        func_def = collect_function_definitions_rec(self._tree.root_node)
        func_def.extend(self._collect_macro_definitions())

        return func_def
    
    def _collect_macro_definitions(self):
        """
        Recursively collect macro definition nodes from the syntax tree along with their names and start/end lines.

        :return: A list of tuples, each containing the node, the name of the macro, and its start and end line numbers.
        """

        macro_definitions = []

        def collect_macro_definitions_recursive(node):

            if node.type == "preproc_function_def":  # preproc_def = #define in C but for numbers/constants
                content = self._slice(node.start_byte, node.end_byte)

                # `#define` and also `#    define` (indented inside #ifdef blocks, as in FFmpeg)
                if re.match(r"#\s*define\b", content):
                    name_node = node.child_by_field_name("name")
                    if name_node is not None:
                        macro_name = self._slice(name_node.start_byte, name_node.end_byte)
                    else:
                        parts = content.split(maxsplit=2)
                        macro_name = parts[1].split('(')[0] if len(parts) >= 2 else ""
                    if macro_name:
                        start_line = node.start_point[0]
                        end_line = node.end_point[0]
                        macro_definitions.append((node, macro_name, start_line, end_line))

            for child in node.children:
                collect_macro_definitions_recursive(child)

            return macro_definitions

        return collect_macro_definitions_recursive(self._tree.root_node)
    
    def get_function_name(self, node) -> str:
        """
        Extract the name of a function node.

        :param node: The function node.
        :return: The name of the function.
        """
        #  Search for function_declarator node within function_definition node
        function_declarator_node = self._find_function_declarator(node)
        if function_declarator_node is None:
            raise RuntimeError('Could not identify the name of the function')
        
        return super().get_function_name(function_declarator_node)
    
    def _find_function_declarator(self, node):
        """
        Find the function_declarator node within a function_definition node.
        Also handles macro-style function definitions like PHP_MINFO_FUNCTION(mcrypt)
        which tree-sitter parses as parenthesized_declarator.

        :param node: The function_definition node.
        :return: The function_declarator node (or parenthesized_declarator for macros).
        """
        if node.type == "function_declarator":
            return node
        # Handle macro-style function definitions like PHP_MINFO_FUNCTION(mcrypt)
        # Tree-sitter parses these as: type_identifier + parenthesized_declarator
        if node.type == "parenthesized_declarator":
            return node
        for child in node.children:
            function_declarator = self._find_function_declarator(child)
            if function_declarator:
                return function_declarator
        return None
    
    def _find_function_type_and_declarator(self, node):
        """
        Find the function_type and function_declarator nodes within a function_definition node.

        :param node: The function_definition node.
        :return: A tuple containing the function_type and function_declarator nodes, or (None, None) if not found.
        """
        function_type_node = None
        function_declarator_node = None

        function_declarator_node = self._find_function_declarator(node)
        if function_declarator_node:
            function_type_node = function_declarator_node.parent.children[0]
            if function_type_node is None:
                return None, function_declarator_node
            else:
                return function_type_node, function_declarator_node

        # No function_declarator found - return None tuple instead of implicit None
        return None, None
    
    def extract_method_details(self, nodes):
        method_invocation_node = None
        for node in nodes:
            if node.type == 'call_expression':
                method_invocation_node = node
                break

        if not method_invocation_node:
            return {
                'method_parts': [],
                'arguments': []
            }

        method_parts = super().get_method_parts(method_invocation_node)
        arguments = super().get_arguments(method_invocation_node)

        return {
            'method_parts': method_parts,
            'arguments': arguments
        }
    
    def get_function_info(self, line_number):
        """
        Get the function name and the line range of the function containing the specified line number.

        :param line_number: The target line number.
        :return: A dictionary containing the function name and the line range (lines 0-based).
        """
        function_node = self.find_function_containing_line(line_number)
        if function_node is None:
            return None

        type_node, declarator = self._find_function_type_and_declarator(function_node)

        # Handle case where no declarator was found (e.g., non-C syntax like Objective-C parsed as C)
        if declarator is None:
            # Try multiple fallback strategies to get a meaningful name
            function_name = None
            name_raw = None

            # Strategy 1: Try the base class method
            try:
                function_name = self.get_function_name(function_node)
                name_raw = function_name
            except RuntimeError:
                pass

            # Strategy 2: Look for any identifier directly in the function_node's children
            # This handles cases like Objective-C "@interface Foo" parsed as C,
            # where tree-sitter sees it as: type_identifier("interface") + identifier("Foo")
            if function_name is None:
                for child in function_node.children:
                    if child.type == "identifier":
                        name_raw = child.text.decode('utf-8')
                        # Also check for type prefix (like "interface" in Objective-C)
                        type_child = function_node.child_by_field_name('type')
                        if type_child:
                            function_name = f"{type_child.text.decode('utf-8')} {name_raw}"
                        else:
                            function_name = name_raw
                        break

            # Strategy 3: Extract first identifier anywhere in the subtree
            if function_name is None:
                name_raw = self._extract_identifier_from_node(function_node)
                if name_raw:
                    function_name = name_raw

            # Last resort: use a generic name with line number for uniqueness
            if function_name is None:
                start_line = function_node.start_point[0]
                function_name = f"unknown_at_line_{start_line}"
                name_raw = function_name

            start_line = function_node.start_point[0]
            end_line = function_node.end_point[0]

            return {
                'name': function_name,
                'name_raw': name_raw,
                'start_line': start_line,
                'end_line': end_line,
                'node': function_node
            }

        if type_node is None:
            function_name = self.get_text_from_node(declarator).strip()
        else:
            function_name = self.get_text_from_node(type_node).strip() + ' ' + self.get_text_from_node(declarator).strip()

        start_line = function_node.start_point[0]
        end_line = function_node.end_point[0]

        # Extract raw name - handle both function_declarator and parenthesized_declarator
        name_raw = None
        if declarator.type == "function_declarator":
            # Standard function: use 'declarator' field which contains the name
            name_field = declarator.child_by_field_name('declarator')
            if name_field:
                name_raw = name_field.text.decode('utf-8')
        elif declarator.type == "parenthesized_declarator":
            # Macro-style function like PHP_MINFO_FUNCTION(mcrypt)
            # Tree-sitter parses this as: type_identifier (macro name) + parenthesized_declarator (argument)
            # To ensure uniqueness, combine macro name with argument: "PHP_MINFO_FUNCTION_mcrypt"
            # This prevents collisions when same argument is used with different macros
            # (e.g., PHP_MINFO_FUNCTION(mcrypt) vs PHP_MINIT_FUNCTION(mcrypt))
            macro_name = type_node.text.decode('utf-8') if type_node else ""
            arg_name = None
            for child in declarator.children:
                if child.type == "identifier":
                    arg_name = child.text.decode('utf-8')
                    break
            if macro_name and arg_name:
                name_raw = f"{macro_name}_{arg_name}"
            elif arg_name:
                name_raw = arg_name

        # Fallback if we couldn't extract the raw name
        if name_raw is None:
            # Try to find any identifier in the declarator
            name_raw = self._extract_identifier_from_node(declarator)
            if name_raw is None:
                name_raw = function_name  # Last resort: use full function name

        return {
            'name': function_name,
            'name_raw': name_raw,
            'start_line': start_line,
            'end_line': end_line,
            'node': function_node
        }

    def _extract_identifier_from_node(self, node):
        """
        Recursively find the first identifier in a node.
        """
        if node.type == "identifier":
            return node.text.decode('utf-8')
        for child in node.children:
            result = self._extract_identifier_from_node(child)
            if result:
                return result
        return None
    
    def get_function_calls(self, root):
        """
        Get all functions called in the syntax tree of a node/function.
        """
        function_calls = []

        stack = [root]

        while stack:
            node = stack.pop()

            if node.type == 'call_expression':
                method_name_node = None
                # Use a local stack to find the last identifier before 'argument_list'
                local_stack = list(node.children)
                while local_stack:
                    child = local_stack.pop(0)  # Treat as a queue; change pop(0) to pop() for stack behavior
                    if child.type == 'identifier':
                        method_name_node = child
                    elif child.type == 'argument_list':
                        break  # Stop if we reach the argument list

                if method_name_node:
                    function_name = super().get_text_from_node(method_name_node)
                    function_calls.append((function_name, method_name_node.start_point[0] + 1))  # Convert to 1-based line number

            # Add children to the stack to process them next
            stack.extend(node.children)

        return function_calls
    
    def get_function_details(self, node):
        """
        Extract the function name and parameters from a function definition node.

        :param node: The function definition node.
        :return: A dictionary containing the name of the function and the number of parameters
        """
        if node.type == 'function_definition':
            method_name = self.get_function_name(node)
            parameters = 0
            void_parameter = False

            for child in node.children:
                if child.type == 'function_declarator':
                    for childre in child.children:
                        if childre.type == 'parameter_list':
                            # check if parameter_list has only one child with type 'parameter_declaration'
                            parameter_decl = [chi for chi in childre.children if chi.type == 'parameter_declaration']
                            if len(parameter_decl) == 1:
                                param_node = parameter_decl[0]
                                if super().get_text_from_node(param_node) == 'void':
                                    void_parameter = True
                                    continue

                            for chi in childre.children:
                                if chi.type == 'parameter_declaration':
                                    if super().get_text_from_node(chi) != 'void':
                                        parameters += 1

            return {
                'name': method_name,
                'parameters': parameters
            }
    
    def get_hierarchical_context_for_line(self, line_number: int):
        """
        Get hierarchical context for a line using priority:
        1. Function context (highest priority)
        2. Struct context (if not in function but in struct)  
        3. Global context (if not in function and not in struct)
        """
        # First priority: Check if we're inside a function
        function_info = self.get_function_info(line_number)
        if function_info:
            return {
                'type': 'function',
                'name': function_info['name_raw'],
                'full_context': function_info['name_raw'],
                'function': function_info
            }
        
        # Second priority: Check if we're inside a struct (but not in a function)
        # struct_node = self._find_struct_containing_line(line_number - 1)  # Convert to 0-based
        # if struct_node:
        #     struct_name = self._get_struct_name(struct_node)
        #     return {
        #         'type': 'struct',
        #         'name': struct_name,
        #         'full_context': struct_name,
        #         'function': None
        #     }
        
        # Third priority: Global context
        return {
            'type': '__global_context__',
            'name': '__global_context__',
            'full_context': '__global_context__',
            'function': None
        }
    
    def _find_struct_containing_line(self, target_line):
        """
        Find struct node that contains the target line.
        """
        for node in self._walk_tree(self._tree.root_node):
            if node.type == "struct_specifier":
                if node.start_point[0] <= target_line <= node.end_point[0]:
                    return node
        return None
    
    def _get_struct_name(self, struct_node):
        """
        Extract the name of a struct node.
        """
        try:
            # Look for the struct name (might be in type_identifier)
            for child in struct_node.children:
                if child.type == "type_identifier":
                    return child.text.decode('utf-8')
            
            # If no name found, use anonymous struct
            return "anonymous_struct"
        except:
            return "anonymous_struct"
    
    def _walk_tree(self, node):
        """
        Generator to walk through all nodes in the tree.
        """
        yield node
        for child in node.children:
            yield from self._walk_tree(child)
