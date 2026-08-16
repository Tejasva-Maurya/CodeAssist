import tree_sitter_html as tshtml
from tree_sitter import Language, Parser, Query, QueryCursor
from .base import BaseExtractor, FileEntity, HtmlNodeEntity, CommentEntity

class HtmlExtractor(BaseExtractor):
    def __init__(self):
        super().__init__("html")
        self.LANGUAGE = Language(tshtml.language())
        self.parser = Parser(self.LANGUAGE)
        
        # Query for all start tags
        self.start_tag_query = Query(self.LANGUAGE, """
            (start_tag) @tag
        """)
        
        self.comment_query = Query(self.LANGUAGE, """
            (comment) @comment
        """)

    def _extract_attributes(self, start_tag_node, content: bytes) -> dict:
        attrs = {}
        for child in start_tag_node.children:
            if child.type == "attribute":
                name = None
                value = None
                for attr_child in child.children:
                    if attr_child.type == "attribute_name":
                        name = content[attr_child.start_byte:attr_child.end_byte].decode('utf8').lower()
                    elif attr_child.type == "quoted_attribute_value":
                        # The value is inside the quotes, so we check for attribute_value
                        for val_child in attr_child.children:
                            if val_child.type == "attribute_value":
                                value = content[val_child.start_byte:val_child.end_byte].decode('utf8')
                if name:
                    attrs[name] = value if value is not None else ""
        return attrs

    def parse_file(self, filepath: str, content: bytes) -> FileEntity:
        tree = self.parser.parse(content)
        root_node = tree.root_node
        
        file_entity = FileEntity(filepath=filepath)
        
        # Extract comments
        for _, captures in QueryCursor(self.comment_query).matches(root_node):
            if "comment" in captures:
                for node in captures["comment"]:
                    file_entity.comments.append(CommentEntity(
                        text=content[node.start_byte:node.end_byte].decode('utf8').strip(),
                        start_line=node.start_point[0] + 1,
                        end_line=node.end_point[0] + 1
                    ))
                    
        # Extract tags
        INTERACTIONS = {"button", "input", "form", "a"}
        CONTAINERS = {"div", "section", "header", "footer", "nav", "main", "article"}
        
        for _, captures in QueryCursor(self.start_tag_query).matches(root_node):
            if "tag" in captures:
                for node in captures["tag"]:
                    # Get tag name
                    tag_name_node = None
                    for child in node.children:
                        if child.type == "tag_name":
                            tag_name_node = child
                            break
                            
                    if not tag_name_node:
                        continue
                        
                    tag_name = content[tag_name_node.start_byte:tag_name_node.end_byte].decode('utf8').lower()
                    attrs = self._extract_attributes(node, content)
                    
                    # 1. Check for Dependencies (Scripts, Styles)
                    if tag_name == "script" and "src" in attrs:
                        file_entity.imports.append(attrs["src"])
                    elif tag_name == "link" and attrs.get("rel") == "stylesheet" and "href" in attrs:
                        file_entity.imports.append(attrs["href"])
                        
                    # 2. Check for Interactions and Containers
                    if tag_name in INTERACTIONS or (tag_name in CONTAINERS and "id" in attrs):
                        node_type = "interaction" if tag_name in INTERACTIONS else "container"
                        file_entity.html_nodes.append(HtmlNodeEntity(
                            tag=tag_name,
                            id_attr=attrs.get("id"),
                            class_attr=attrs.get("class"),
                            node_type=node_type,
                            start_line=node.start_point[0] + 1,
                            end_line=node.end_point[0] + 1
                        ))
                        
        return file_entity
