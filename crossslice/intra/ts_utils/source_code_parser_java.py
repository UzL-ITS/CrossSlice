"""
This module is used to parse the source code of Java language using tree-sitter.
It's based on the SourceCodeParser class that is used to parse the source code of Java and C language.
"""
from .source_code_parser import SourceCodeParser

class SourceCodeParserJava(SourceCodeParser):
    
    def __init__(self, file_path: str):
        if not file_path.endswith(".java"):
            raise NotImplementedError("File is not a Java file: " + file_path)
        
        super().__init__(file_path)

    def collect_function_definitions(self) -> list[tuple]:
        """
        Recursively collect function definition nodes from the syntax tree along with their names and start/end lines.
        For Java, this includes methods, constructors, and compact constructors.

        :return: A list of tuples: (node, function_name, start_line, end_line)
        """
        function_definitions = []

        def collect_function_definitions_rec(node):
            # Java method declarations
            if node.type == "method_declaration":
                function_name = self.get_function_name(node)
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                function_definitions.append((node, function_name, start_line, end_line))
            
            # Java constructor declarations
            elif node.type == "constructor_declaration":
                function_name = self.get_constructor_name(node)
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                function_definitions.append((node, function_name, start_line, end_line))
            
            # Java compact constructor declarations (for records)
            elif node.type == "compact_constructor_declaration":
                function_name = self.get_compact_constructor_name(node)
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                function_definitions.append((node, function_name, start_line, end_line))

            for child in node.children:
                collect_function_definitions_rec(child)

            return function_definitions
        
        return collect_function_definitions_rec(self._tree.root_node)

    def collect_class_definitions(self) -> list[tuple]:
        """
        Recursively collect class definition nodes from the syntax tree along with their names and start/end lines.
        This includes classes, interfaces, enums, and records.

        :return: A list of tuples: (node, class_name, start_line, end_line)
        """
        class_definitions = []

        def collect_class_definitions_rec(node):
            if node.type in ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration"]:
                class_name = self.get_class_name(node)
                start_line = node.start_point[0]
                end_line = node.end_point[0]
                class_definitions.append((node, class_name, start_line, end_line))

            for child in node.children:
                collect_class_definitions_rec(child)

            return class_definitions
        
        return collect_class_definitions_rec(self._tree.root_node)

    def get_function_name(self, node) -> str:
        """
        Extract the name of a method node.

        :param node: The method declaration node.
        :return: The name of the method.
        """
        if node.type == "method_declaration":
            name_node = node.child_by_field_name('name')
            if name_node:
                return name_node.text.decode('utf-8')
        
        return super().get_function_name(node)
    
    def get_constructor_name(self, node) -> str:
        """
        Extract the name of a constructor node.

        :param node: The constructor declaration node.
        :return: The name of the constructor.
        """
        if node.type == "constructor_declaration":
            name_node = node.child_by_field_name('name')
            if name_node:
                return name_node.text.decode('utf-8')
        
        raise RuntimeError('Could not identify the name of the constructor')
    
    def get_compact_constructor_name(self, node) -> str:
        """
        Extract the name of a compact constructor node (for records).

        :param node: The compact constructor declaration node.
        :return: The name of the compact constructor.
        """
        if node.type == "compact_constructor_declaration":
            name_node = node.child_by_field_name('name')
            if name_node:
                return name_node.text.decode('utf-8')
        
        raise RuntimeError('Could not identify the name of the compact constructor')
    
    def get_class_name(self, node) -> str:
        """
        Extract the name of a class/interface/enum/record node.

        :param node: The class declaration node.
        :return: The name of the class.
        """
        if node.type in ["class_declaration", "interface_declaration", "enum_declaration", "record_declaration"]:
            name_node = node.child_by_field_name('name')
            if name_node:
                return name_node.text.decode('utf-8')
        
        raise RuntimeError('Could not identify the name of the class')

    def find_function_containing_line(self, line_number: int):
        """
        Find the function that contains the specified line number.
        For Java, this includes methods, constructors, and compact constructors.

        :param line_number: The target line number (1-based).
        :return: The function node containing the line, or None if not found.
        """
        function_definitions = self.collect_function_definitions()
        
        # Convert to 0-based for comparison with AST
        target_line = line_number - 1
        
        for node, function_name, start_line, end_line in function_definitions:
            if start_line <= target_line <= end_line:
                return node
        
        return None

    def find_class_containing_line(self, line_number: int):
        """
        Find the class that contains the specified line number.

        :param line_number: The target line number (1-based).
        :return: The class node containing the line, or None if not found.
        """
        class_definitions = self.collect_class_definitions()
        
        # Convert to 0-based for comparison with AST
        target_line = line_number - 1
        
        for node, class_name, start_line, end_line in class_definitions:
            if start_line <= target_line <= end_line:
                return node
        
        return None

    def get_hierarchical_context_for_line(self, line_number: int) -> dict:
        """
        Get hierarchical context for a line using priority:
        1. Function/method context (highest priority)
        2. Class context (if not in function but in class)  
        3. Global context (if not in function and not in class)
        
        For method overloading, includes parameter types in the name.
        """
        # Convert to 0-based for AST comparison
        # target_line = line_number - 1
        line_number = line_number + 1
        
        # First priority: Check if we're inside a function/method
        function_node = self.find_function_containing_line(line_number)
        if function_node:
            if function_node.type == "method_declaration":
                function_name = self.get_function_name(function_node)
            elif function_node.type == "constructor_declaration":
                function_name = self.get_constructor_name(function_node)
            elif function_node.type == "compact_constructor_declaration":
                function_name = self.get_compact_constructor_name(function_node)
            else:
                function_name = "unknown_function"
            
            # Handle method overloading by including parameter signature
            if function_node.type in ["method_declaration", "constructor_declaration", "compact_constructor_declaration"]:
                signature = self._get_parameter_signature(function_node)
                unique_name = f"{function_name}{signature}"
            else:
                unique_name = function_name
            
            # Find containing class for full context
            class_node = self.find_class_containing_line(line_number)
            if class_node:
                class_name = self.get_class_name(class_node)
                full_context = f"{class_name}.{unique_name}"
            else:
                full_context = unique_name
            
            return {
                'type': 'function',
                'name': unique_name,
                'full_context': full_context,
                'function': {
                    'name_raw': function_name,
                    'name': unique_name,
                    'node': function_node,
                    'start_line': function_node.start_point[0],
                    'end_line': function_node.end_point[0]
                }
            }
        
        # Second priority: Check if we're inside a class (but not in a method)
        class_node = self.find_class_containing_line(line_number)
        if class_node:
            class_name = self.get_class_name(class_node)
            return {
                'type': 'class',
                'name': class_name,
                'full_context': class_name,
                'function': None,
                'class': {
                    'name_raw': class_name,
                    'name': class_name,
                    'node': class_node,
                    'start_line': class_node.start_point[0],
                    'end_line': class_node.end_point[0]
                }
            }
        
        # Third priority: Global context
        return {
            'type': '__global_context__',
            'name': '__global_context__',
            'full_context': '__global_context__',
            'function': None
        }
    
    def _get_parameter_signature(self, method_node):
        """
        Extract method parameter signature for overloading disambiguation.
        Returns something like "(int,String)" or "()" for no parameters.
        """
        try:
            params_node = method_node.child_by_field_name('parameters')
            if not params_node:
                return "()"
            
            param_types = []
            for child in params_node.children:
                if child.type == "formal_parameter":
                    type_node = child.child_by_field_name('type')
                    if type_node:
                        type_text = type_node.text.decode('utf-8').strip()
                        param_types.append(type_text)
            
            if not param_types:
                return "()"
            return f"({','.join(param_types)})"
        except:
            return "()"

    def extract_method_details(self, nodes):
        """
        Extract method invocation details from nodes.
        For Java, this handles method calls including chained calls.
        """
        method_invocation_node = None
        for node in nodes:
            if node.type == 'method_invocation':
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
        Get the function/class name and the line range of the function/class containing the specified line number.
        For Java, this handles methods, constructors, compact constructors, and classes.
        
        :param line_number: The target line number (0-based).
        :return: A dictionary containing the function/class name and the line range (lines 0-based).
        """
        # First try to find a function (method, constructor, etc.)
        # Convert 0-based to 1-based for the existing helper functions
        function_node = self.find_function_containing_line(line_number + 1)
        if function_node is not None:
            # Get function signature based on type
            if function_node.type == "method_declaration":
                function_name = self._get_method_signature(function_node)
                raw_name = self.get_function_name(function_node)
            elif function_node.type == "constructor_declaration":
                function_name = self._get_constructor_signature(function_node)
                raw_name = self.get_constructor_name(function_node)
            elif function_node.type == "compact_constructor_declaration":
                function_name = self._get_compact_constructor_signature(function_node)
                raw_name = self.get_compact_constructor_name(function_node)
            else:
                function_name = self.get_text_from_node(function_node).strip()
                raw_name = "unknown"

            start_line = function_node.start_point[0]
            end_line = function_node.end_point[0]

            return {
                'name': function_name,
                'name_raw': raw_name,
                'start_line': start_line,
                'end_line': end_line,
                'node': function_node
            }
        
        # If no function found, try to find a class
        # Convert 0-based to 1-based for the existing helper functions
        class_node = self.find_class_containing_line(line_number + 1)
        if class_node is not None:
            class_name = self.get_class_name(class_node)
            start_line = class_node.start_point[0]
            end_line = class_node.end_point[0]

            return {
                'name': class_name,
                'name_raw': class_name,
                'start_line': start_line,
                'end_line': end_line,
                'node': class_node
            }
        
        # If neither function nor class found, return None
        return None

    def _get_method_signature(self, node) -> str:
        """
        Extract method signature including return type, name, and parameters.
        """
        if node.type != "method_declaration":
            return self.get_text_from_node(node).strip()
        
        # Get modifiers (if any)
        modifiers_node = node.child_by_field_name('modifiers')
        modifiers = self.get_text_from_node(modifiers_node).strip() if modifiers_node else ""
        
        # Get return type
        type_node = node.child_by_field_name('type')
        return_type = self.get_text_from_node(type_node).strip() if type_node else "void"
        
        # Get method name
        name_node = node.child_by_field_name('name')
        method_name = self.get_text_from_node(name_node).strip() if name_node else "unknown"
        
        # Get parameters
        parameters_node = node.child_by_field_name('parameters')
        parameters = self.get_text_from_node(parameters_node).strip() if parameters_node else "()"
        
        # Combine into signature
        signature_parts = [part for part in [modifiers, return_type, method_name + parameters] if part]
        return " ".join(signature_parts)

    def _get_constructor_signature(self, node) -> str:
        """
        Extract constructor signature including modifiers, name, and parameters.
        """
        if node.type != "constructor_declaration":
            return self.get_text_from_node(node).strip()
        
        # Get modifiers (if any)
        modifiers_node = node.child_by_field_name('modifiers')
        modifiers = self.get_text_from_node(modifiers_node).strip() if modifiers_node else ""
        
        # Get constructor name
        name_node = node.child_by_field_name('name')
        constructor_name = self.get_text_from_node(name_node).strip() if name_node else "unknown"
        
        # Get parameters
        parameters_node = node.child_by_field_name('parameters')
        parameters = self.get_text_from_node(parameters_node).strip() if parameters_node else "()"
        
        # Combine into signature
        signature_parts = [part for part in [modifiers, constructor_name + parameters] if part]
        return " ".join(signature_parts)

    def _get_compact_constructor_signature(self, node) -> str:
        """
        Extract compact constructor signature (for records).
        """
        if node.type != "compact_constructor_declaration":
            return self.get_text_from_node(node).strip()
        
        # Get modifiers (if any)
        modifiers_node = node.child_by_field_name('modifiers')
        modifiers = self.get_text_from_node(modifiers_node).strip() if modifiers_node else ""
        
        # Get constructor name
        name_node = node.child_by_field_name('name')
        constructor_name = self.get_text_from_node(name_node).strip() if name_node else "unknown"
        
        # Compact constructors don't have explicit parameters (they inherit from record)
        # Combine into signature
        signature_parts = [part for part in [modifiers, constructor_name + "()"] if part]
        return " ".join(signature_parts)
    
    def get_function_calls(self, root):
        """
        Get all method calls in the syntax tree of a node/function.
        For Java, this includes method invocations and constructor calls.
        """
        function_calls = []
        stack = [root]

        while stack:
            node = stack.pop()

            if node.type == 'method_invocation':
                method_name_node = node.child_by_field_name('name')
                if method_name_node:
                    function_name = self.get_text_from_node(method_name_node)
                    function_calls.append((function_name, method_name_node.start_point[0] + 1))
            
            elif node.type == 'object_creation_expression':
                # Constructor calls
                type_node = node.child_by_field_name('type')
                if type_node:
                    constructor_name = self.get_text_from_node(type_node)
                    function_calls.append((f"new {constructor_name}", type_node.start_point[0] + 1))

            # Add children to the stack to process them next
            stack.extend(node.children)

        return function_calls
    
    def get_function_details(self, node):
        """
        Extract the function name and parameters from a function definition node.
        For Java, this handles methods, constructors, and compact constructors.

        :param node: The function definition node.
        :return: A dictionary containing the name of the function and the number of parameters
        """
        if node.type in ['method_declaration', 'constructor_declaration', 'compact_constructor_declaration']:
            if node.type == 'method_declaration':
                method_name = self.get_function_name(node)
            elif node.type == 'constructor_declaration':
                method_name = self.get_constructor_name(node)
            elif node.type == 'compact_constructor_declaration':
                method_name = self.get_compact_constructor_name(node)
            
            parameters = 0
            
            # Find parameters node
            parameters_node = node.child_by_field_name('parameters')
            if parameters_node:
                # Count formal parameters
                for child in parameters_node.children:
                    if child.type in ['formal_parameter', 'spread_parameter']:
                        parameters += 1

            return {
                'name': method_name,
                'parameters': parameters
            }
        
        return {
            'name': 'unknown',
            'parameters': 0
        }

    def get_class_info(self, line_number):
        """
        Get the class name and the line range of the class containing the specified line number.
        
        :param line_number: The target line number.
        :return: A dictionary containing the class name and the line range (lines 0-based).
        """
        class_node = self.find_class_containing_line(line_number)
        if class_node is None:
            return None

        class_name = self.get_class_name(class_node)
        start_line = class_node.start_point[0]
        end_line = class_node.end_point[0]

        return {
            'name': class_name,
            'start_line': start_line,
            'end_line': end_line,
            'node': class_node,
            'type': class_node.type
        }

    def get_all_hierarchical_contexts(self):
        """
        Get all hierarchical contexts (classes, methods, constructors) in the file.
        Returns a list of context objects similar to get_hierarchical_context_for_line.
        
        Returns:
            List of context dictionaries with 'type', 'name', 'full_context', 'function', 'class' keys
        """
        contexts = []
        
        # Get all classes
        class_definitions = self.collect_class_definitions()
        for class_node, class_name, start_line, end_line in class_definitions:
            class_context = {
                'type': 'class',
                'name': class_name,
                'full_context': class_name,
                'function': None,
                'class': {
                    'name': class_name,
                    'start_line': start_line + 1,  # Convert to 1-based
                    'end_line': end_line + 1,
                    'node': class_node
                }
            }
            contexts.append(class_context)
            
            # Get all functions/methods within this class
            function_definitions = self.collect_function_definitions()
            for func_node, func_name, func_start, func_end in function_definitions:
                # Check if this function is within the current class
                if start_line <= func_start <= end_line:
                    # Get function signature with parameters
                    func_signature = self._get_parameter_signature(func_node)
                    full_func_name = f"{func_name}{func_signature}" if func_signature else func_name
                    
                    function_context = {
                        'type': 'function',
                        'name': full_func_name,
                        'full_context': f"{class_name}.{full_func_name}",
                        'function': {
                            'name': full_func_name,
                            'name_raw': func_name,
                            'start_line': func_start + 1,  # Convert to 1-based
                            'end_line': func_end + 1,
                            'node': func_node
                        },
                        'class': {
                            'name': class_name,
                            'start_line': start_line + 1,
                            'end_line': end_line + 1,
                            'node': class_node
                        }
                    }
                    contexts.append(function_context)
        
        # Get functions not in any class (should be rare in Java but possible)
        function_definitions = self.collect_function_definitions()
        for func_node, func_name, func_start, func_end in function_definitions:
            # Check if this function is NOT within any class
            in_class = False
            for class_node, class_name, class_start, class_end in class_definitions:
                if class_start <= func_start <= class_end:
                    in_class = True
                    break
            
            if not in_class:
                func_signature = self._get_parameter_signature(func_node)
                full_func_name = f"{func_name}{func_signature}" if func_signature else func_name
                
                function_context = {
                    'type': 'function',
                    'name': full_func_name,
                    'full_context': full_func_name,
                    'function': {
                        'name': full_func_name,
                        'name_raw': func_name,
                        'start_line': func_start + 1,
                        'end_line': func_end + 1,
                        'node': func_node
                    },
                    'class': None
                }
                contexts.append(function_context)
        
        return contexts


if __name__ == "__main__":
    # Example usage
    parser = SourceCodeParserJava("/path/to/test.java")
    
    # Test context detection
    context = parser.get_context_for_line(10)
    print(f"Line 10 context: {context}")
    
    # Test function collection
    functions = parser.collect_function_definitions()
    print(f"Found {len(functions)} functions")
    
    # Test class collection
    classes = parser.collect_class_definitions()
    print(f"Found {len(classes)} classes")
