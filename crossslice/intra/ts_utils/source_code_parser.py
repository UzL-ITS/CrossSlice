# from tree_sitter_languages import get_parser
import tree_sitter_java as ts_java
import tree_sitter_c as ts_c
from tree_sitter import Language, Parser

class SourceCodeParser:
    def __init__(self, file_path: str):
        self._code = None
        self._tree = None
        self._file_path = file_path
        self.parse_file()

    def parse_file(self) -> None:
        """
        Parse a source code file and return the syntax tree.

        :return: syntax tree as tree-sitter node
        """

        # C, C++ and Java
        C_EXTENSIONS = (".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx")
        if not self._file_path.endswith(C_EXTENSIONS) and not self._file_path.endswith(".java"):
            raise NotImplementedError("File is not a C/C++ or Java file: " + self._file_path)

        # parse the file
        parser = Parser(self._language_for(self._file_path))
        try:
            # try to laod the file as UTF-8
            with open(self._file_path, "r") as f:
                self._code = f.read()
        except UnicodeDecodeError as e:
            # if it fails, try to load the file as ISO-8859-1
            with open(self._file_path, "r", encoding="ISO-8859-1") as f:
                self._code = f.read()
        # tree-sitter offsets (start_byte/end_byte, point columns) are BYTE offsets
        # into exactly these bytes; slicing the decoded str with them is wrong as
        # soon as a file contains a non-ASCII character (see _slice).
        self._code_bytes = bytes(self._code, "utf8")
        self._tree = parser.parse(self._code_bytes)

    @staticmethod
    def _language_for(file_path: str) -> Language:
        if file_path.endswith((".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx")):
            return Language(ts_c.language())
        if file_path.endswith(".java"):
            return Language(ts_java.language())
        raise NotImplementedError("File is not a C/C++ or Java file: " + file_path)

    @classmethod
    def from_source(cls, code: str, file_path: str):
        """A parser over `code` as if it were the content of `file_path` (the
        extension selects the language; nothing is read from disk)."""
        self = cls.__new__(cls)
        self._code = code
        self._file_path = file_path
        self._code_bytes = bytes(code, "utf8")
        self._tree = Parser(cls._language_for(file_path)).parse(self._code_bytes)
        return self

    def _slice(self, start_byte: int, end_byte: int) -> str:
        """Source text between two tree-sitter byte offsets."""
        return self._code_bytes[start_byte:end_byte].decode("utf8", errors="replace")

    def get_code(self) -> str:
        return self._code

    def get_source_bytes(self) -> bytes:
        """
        Get the source code as bytes.

        :return: The source code as bytes.
        """
        if self._code is None:
            raise ValueError("Source code not loaded. Call parse_file() first.")
        return bytes(self._code, "utf8")

    def get_top_level_node(self):
        """
        Get the top-level node of the syntax tree.

        :return: The root node of the syntax tree.
        """
        if self._tree is None:
            raise ValueError("Syntax tree not initialized. Call parse_file() first.")
        return self._tree.root_node
    
    def get_function_source_code(self, function_node):
        """
        Extract the source code for a given function node.

        :param function_node: The node representing the function in the syntax tree.
        :return: The source code of the function as a string.
        """
        start = function_node.start_byte
        end = function_node.end_byte
        function_source_code = self._slice(start, end)
        return function_source_code
    
    def collect_function_definitions(self) -> list[tuple]:
        """
        Recursively collect function definition nodes from the syntax tree along with their names and start/end lines.

        :return: A list of tuples, each containing the node, the name of the function, and its start and end line numbers.
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
        
        return collect_function_definitions_rec(self._tree.root_node)
    
    def get_function_name(self, node) -> str:
        """
        Extract the name of a function node.

        :param node: The function node.
        :return: The name of the function.
        """
        function_name_node = self._find_function_name_node(node)
        if function_name_node is None:
            raise RuntimeError('Could not identify the name of the calling function')

        function_name = self._slice(function_name_node.start_byte, function_name_node.end_byte)
        return function_name
    
    def _find_function_name_node(self, node):
        """
        Attempt to find the function name node within a function definition node.

        :param node: A Tree-sitter node representing a part of the function definition.
        :return: The node containing the function name, or None if not found.
        """
        if node.type == 'identifier' and node.parent.type != 'marker_annotation':
            return node
        for child in node.children:
            result = self._find_function_name_node(child)
            if result is not None:
                return result
        return None
    
    def get_method_parts(self, method_invocation_node):
        method_parts = []
        for child in method_invocation_node.children:
            if child.type == 'identifier':
                method_parts.append(self.get_text_from_node(child))
            elif child.type == 'argument_list':
                break
        return method_parts
    
    def get_arguments(self, method_invocation_node):
        """
        Extract the arguments from a method invocation node.
        """
        arguments = []
        # Find the 'argument_list' within the 'call_expression'
        argument_list = next((child for child in method_invocation_node.children if child.type == 'argument_list'), None)
        if argument_list:
            collect = False  # Flag to start collecting nodes after '('
            # Iterate through all children nodes within the argument list
            for child in argument_list.children:
                if child.type == '(':
                    collect = True  # Start collecting after '('
                    continue
                elif child.type == ')':
                    break  # Stop collecting before ')'
                
                if collect and child.type not in [',', '(', ')']:  # Ignore commas and parentheses
                    argument_text = self.get_text_from_node(child)
                    arguments.append({
                        'type': child.type,
                        'value': argument_text
                    })

        return arguments
    
    def get_text_from_node(self, node):
        """
        Extract the text content from a node using the source code.
        """
        start_byte = node.start_byte
        end_byte = node.end_byte
        return self._slice(start_byte, end_byte)
    
    def find_function_containing_line(self, line_number):
        """
        Search for the function node that contains the specified line number.

        :param line_number: The target line number.
        :return: The node of the function containing the line, or None if not found.
        """
        if self._tree is None:
            raise ValueError("Syntax tree not initialized. Call parse_file() first.")

        return self._find_function_containing_line(self._tree.root_node, line_number)

    def _find_function_containing_line(self, node, line_number):
        """
        Recursively search for the function node that contains the specified line number.

        :param node: The current node in the syntax tree.
        :param line_number: The target line number, 1-based.
        :return: The node of the function containing the line, or None if not found.
        """
        start_line = node.start_point[0]
        end_line = node.end_point[0]
        if end_line < line_number:
            return None
        if start_line > line_number:
            return None

        #print(node.type)
        if "function_definition" == node.type or "method_declaration" == node.type:
            if start_line <= line_number <= end_line:
                return node

        for child in node.children:
            result = self._find_function_containing_line(child, line_number)
            if result is not None:
                return result

        return None
    
    def get_function_info(self, line_number):
        """
        Get the function name and the line range of the function containing the specified line number.
        
        :param line_number: The target line number.
        :return: A dictionary containing the function name and the line range (lines 1-based).
        """
        function_node = self.find_function_containing_line(line_number - 1)
        if function_node is None:
            return None

        function_name = self.get_function_name(function_node)
        start_line = function_node.start_point[0]
        end_line = function_node.end_point[0]

        return {
            'name': function_name,
            'start_line': start_line + 1,
            'end_line': end_line + 1
        }

    
    def find_line_node(self, target_line_number):
        """
        Iteratively find the highest-level node that spans exactly the target line number
        and whose parent does not also span exactly that line.

        :param target_line_number: The target line number (1-based).
        :return: The node that spans exactly the target line, or None if not found.
        """
        if self._tree is None:
            raise ValueError("Syntax tree not initialized. Call parse_file() first.")

        target_line_zero_based = target_line_number - 1
        stack = [(self._tree.root_node, None)]  # Each item is a tuple (node, parent)

        result_node = None
        context_node = None

        line_nodes = []

        while stack:
            node, parent = stack.pop()
            start_line = node.start_point[0]
            end_line = node.end_point[0]

            # since we start from the root node, we go downwards
            if start_line == target_line_zero_based and context_node is None:
                context_node = node

            # Check if node spans exactly the target line
            if start_line == end_line == target_line_zero_based:
                # Check if parent spans exactly the target line
                parent_spans_line = False
                if parent:
                    parent_start_line = parent.start_point[0]
                    parent_end_line = parent.end_point[0]
                    if parent_start_line == parent_end_line == target_line_zero_based:
                        parent_spans_line = True
                
                # Check if there are any siblings that also span the target line
                for sibling in parent.children:
                    sibling_start_line = sibling.start_point[0]
                    sibling_end_line = sibling.end_point[0]
                    if sibling_start_line == sibling_end_line == target_line_zero_based:
                        # If a sibling spans the target line, this is also a line node
                        line_nodes.append(sibling)

                if not parent_spans_line:
                    # This node is the highest-level node that spans exactly the target line
                    return { 'line_node': line_nodes, 'context_node': context_node }  # Return immediately upon finding the node

                # No need to traverse further down this branch
                continue

            # If node spans the target line (or more), traverse its children
            if start_line <= target_line_zero_based <= end_line:
                for child in reversed(node.children):
                    stack.append((child, node))

        return { 'line_node': line_nodes, 'context_node': context_node }
    
    def print_node_types(self, node, count = 0):
        """
            Iterate through the children of a node and print their types and text content.
        """
        if node.type == "declaration":
            # get the declaration type and declarator
            dec_node = node.child_by_field_name("type")
            print(f"Declaration Type: {self.get_text_from_node(dec_node)}")
            dec_node = node.child_by_field_name("declarator")
            print(f"Declaration Type: {self.get_text_from_node(dec_node)}")
            print(f"type of declaration: {dec_node.type}")
            print(f"Child count: {dec_node.child_count}")

        if count == 0:
            print(f"Node {count} - {node.type}; {self.get_text_from_node(node)}")
        counter = 0
        for child in node.children:
            print(f"Child {counter}:{count} - {child.type}; {self.get_text_from_node(child)}")
            counter += 1

            self.print_node_types(child, counter)
