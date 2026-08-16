import tree_sitter_java as tsjava
from tree_sitter import Language, Parser, Query, QueryCursor
from .base import BaseExtractor, FileEntity, ClassEntity, MethodEntity, CommentEntity

class JavaExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("java")
        self.JAVA_LANGUAGE = Language(tsjava.language())
        self.parser = Parser(self.JAVA_LANGUAGE)
        
        # Define tree-sitter queries for extraction
        self.class_query = Query(self.JAVA_LANGUAGE, """
            (class_declaration 
                name: (identifier) @class.name
            ) @class.def
        """)
        
        self.method_query = Query(self.JAVA_LANGUAGE, """
            (method_declaration
                name: (identifier) @method.name
            ) @method.def
        """)
        
        self.call_query = Query(self.JAVA_LANGUAGE, """
            (method_invocation
                name: (identifier) @call.name
            )
        """)
        
        self.import_query = Query(self.JAVA_LANGUAGE, """
            (import_declaration) @import.def
        """)
        
        self.comment_query = Query(self.JAVA_LANGUAGE, """
            (line_comment) @comment.line
            (block_comment) @comment.block
        """)

    def _extract_methods(self, class_node, content: bytes) -> list[MethodEntity]:
        methods = []
        cursor = QueryCursor(self.method_query)
        matches = cursor.matches(class_node)
        
        # matches returns List[Tuple[int, Dict[str, List[Node]]]]
        for match_idx, captures in matches:
            if "method.def" in captures and "method.name" in captures:
                method_def_node = captures["method.def"][0]
                method_name_node = captures["method.name"][0]
                
                method_name = content[method_name_node.start_byte:method_name_node.end_byte].decode('utf8')
                
                # Extract calls inside this method
                calls = []
                call_cursor = QueryCursor(self.call_query)
                call_matches = call_cursor.matches(method_def_node)
                
                for _, call_captures in call_matches:
                    if "call.name" in call_captures:
                        for call_node in call_captures["call.name"]:
                            calls.append(content[call_node.start_byte:call_node.end_byte].decode('utf8'))
                            
                methods.append(MethodEntity(
                    name=method_name,
                    signature=content[method_def_node.start_byte:method_def_node.end_byte].decode('utf8').split('{')[0].strip(),
                    start_line=method_def_node.start_point[0] + 1,
                    end_line=method_def_node.end_point[0] + 1,
                    calls=list(set(calls))
                ))
                    
        return methods

    def parse_file(self, filepath: str, content: bytes) -> FileEntity:
        tree = self.parser.parse(content)
        root_node = tree.root_node
        
        file_entity = FileEntity(filepath=filepath)
        
        # 1. Extract Imports
        import_cursor = QueryCursor(self.import_query)
        for _, captures in import_cursor.matches(root_node):
            if "import.def" in captures:
                for node in captures["import.def"]:
                    file_entity.imports.append(content[node.start_byte:node.end_byte].decode('utf8').strip())
                
        # 2. Extract Comments
        comment_cursor = QueryCursor(self.comment_query)
        comment_captures = comment_cursor.captures(root_node)
        
        for name, nodes in comment_captures.items():
            for node in nodes:
                file_entity.comments.append(CommentEntity(
                    text=content[node.start_byte:node.end_byte].decode('utf8').strip(),
                    start_line=node.start_point[0] + 1,
                    end_line=node.end_point[0] + 1
                ))
            
        # 3. Extract Classes and their Methods
        class_cursor = QueryCursor(self.class_query)
        for _, captures in class_cursor.matches(root_node):
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
