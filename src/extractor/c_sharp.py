import tree_sitter_c_sharp as tscsharp
from tree_sitter import Language, Parser, Query, QueryCursor
from .base import BaseExtractor, FileEntity, ClassEntity, MethodEntity, CommentEntity

class CSharpExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("c_sharp")
        self.LANGUAGE = Language(tscsharp.language())
        self.parser = Parser(self.LANGUAGE)
        
        self.class_query = Query(self.LANGUAGE, """
            (class_declaration 
                name: (identifier) @class.name
            ) @class.def
        """)
        
        self.method_query = Query(self.LANGUAGE, """
            (method_declaration
                name: (identifier) @method.name
            ) @method.def
        """)
        
        # Matches both local calls Method() and member access obj.Method()
        self.call_query = Query(self.LANGUAGE, """
            (invocation_expression 
                function: [
                    (identifier) @call.name
                    (member_access_expression name: (identifier) @call.name)
                ]
            )
        """)
        
        self.import_query = Query(self.LANGUAGE, """
            (using_directive) @import.def
        """)
        
        self.comment_query = Query(self.LANGUAGE, """
            (comment) @comment
        """)

    def _extract_methods(self, class_node, content: bytes) -> list[MethodEntity]:
        methods = []
        cursor = QueryCursor(self.method_query)
        for _, captures in cursor.matches(class_node):
            if "method.def" in captures and "method.name" in captures:
                method_def_node = captures["method.def"][0]
                method_name_node = captures["method.name"][0]
                
                method_name = content[method_name_node.start_byte:method_name_node.end_byte].decode('utf8')
                
                # Extract calls inside this method
                calls = []
                call_cursor = QueryCursor(self.call_query)
                for _, call_captures in call_cursor.matches(method_def_node):
                    if "call.name" in call_captures:
                        for call_node in call_captures["call.name"]:
                            calls.append(content[call_node.start_byte:call_node.end_byte].decode('utf8'))
                            
                signature_bytes = content[method_def_node.start_byte:method_def_node.end_byte]
                signature = signature_bytes.decode('utf8').split('{')[0].strip()
                            
                methods.append(MethodEntity(
                    name=method_name,
                    signature=signature,
                    start_line=method_def_node.start_point[0] + 1,
                    end_line=method_def_node.end_point[0] + 1,
                    calls=list(set(calls))
                ))
        return methods

    def parse_file(self, filepath: str, content: bytes) -> FileEntity:
        tree = self.parser.parse(content)
        root_node = tree.root_node
        
        file_entity = FileEntity(filepath=filepath)
        
        # Imports
        for _, captures in QueryCursor(self.import_query).matches(root_node):
            if "import.def" in captures:
                for node in captures["import.def"]:
                    file_entity.imports.append(content[node.start_byte:node.end_byte].decode('utf8').strip())
                
        # Comments
        for name, nodes in QueryCursor(self.comment_query).captures(root_node).items():
            for node in nodes:
                file_entity.comments.append(CommentEntity(
                    text=content[node.start_byte:node.end_byte].decode('utf8').strip(),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1
                ))
            
        # Classes
        for _, captures in QueryCursor(self.class_query).matches(root_node):
            if "class.def" in captures and "class.name" in captures:
                class_def_node = captures["class.def"][0]
                class_name_node = captures["class.name"][0]
                
                class_name = content[class_name_node.start_byte:class_name_node.end_byte].decode('utf8')
                methods = self._extract_methods(class_def_node, content)
                
                file_entity.classes.append(ClassEntity(
                    name=class_name,
                    start_line=class_def_node.start_point[0] + 1,
                    end_line=class_def_node.end_point[0] + 1,
                    methods=methods
                ))
                    
        return file_entity
