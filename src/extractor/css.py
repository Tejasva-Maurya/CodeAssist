import tree_sitter_css as tscss
from tree_sitter import Language, Parser, Query, QueryCursor
from .base import BaseExtractor, FileEntity, CssRuleEntity, CommentEntity

class CssExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("css")
        self.LANGUAGE = Language(tscss.language())
        self.parser = Parser(self.LANGUAGE)
        
        self.selector_query = Query(self.LANGUAGE, """
            (class_selector) @selector.class
            (id_selector) @selector.id
        """)
        
        self.import_query = Query(self.LANGUAGE, """
            (import_statement) @import.def
        """)
        
        self.comment_query = Query(self.LANGUAGE, """
            (comment) @comment
        """)

    def parse_file(self, filepath: str, content: bytes) -> FileEntity:
        tree = self.parser.parse(content)
        root_node = tree.root_node
        
        file_entity = FileEntity(filepath=filepath)
        
        # Extract imports
        for _, captures in QueryCursor(self.import_query).matches(root_node):
            if "import.def" in captures:
                for node in captures["import.def"]:
                    text = content[node.start_byte:node.end_byte].decode('utf8')
                    file_entity.imports.append(text.strip())
                    
        # Extract comments
        for _, captures in QueryCursor(self.comment_query).matches(root_node):
            if "comment" in captures:
                for node in captures["comment"]:
                    file_entity.comments.append(CommentEntity(
                        text=content[node.start_byte:node.end_byte].decode('utf8').strip(),
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    ))
                    
        # Extract selectors
        for match_idx, captures in QueryCursor(self.selector_query).matches(root_node):
            for key, nodes in captures.items():
                for node in nodes:
                    selector_text = content[node.start_byte:node.end_byte].decode('utf8')
                    file_entity.css_rules.append(CssRuleEntity(
                        selector=selector_text,
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    ))
                        
        return file_entity
