import uuid
from typing import List
from extractor.base import FileEntity
from storage.graph_base import GraphStorage
from storage.vector_db import VectorStorage

class PipelineLoader:
    """
    Takes extracted FileEntity objects and loads them into 
    the Graph DB (SQLite) and Vector DB (Chroma).
    """
    def __init__(self, graph_db: GraphStorage, vector_db: VectorStorage):
        self.graph_db = graph_db
        self.vector_db = vector_db

    def load_file_entity(self, entity: FileEntity):
        # 1. Add File Node
        file_id = f"file:{entity.filepath}"
        self.graph_db.add_node(
            node_id=file_id,
            label="File",
            properties={"filepath": entity.filepath}
        )

        # 2. Add Comments to Vector DB and Graph DB
        comment_ids = []
        comment_texts = []
        comment_metadatas = []
        
        for idx, comment in enumerate(entity.comments):
            comment_id = f"comment:{entity.filepath}:{comment.start_line}"
            
            # Graph
            self.graph_db.add_node(
                node_id=comment_id,
                label="Comment",
                properties={"text": comment.text, "line": comment.start_line}
            )
            self.graph_db.add_edge(file_id, comment_id, "CONTAINS_COMMENT")
            
            # Vector prep
            comment_ids.append(comment_id)
            comment_texts.append(comment.text)
            comment_metadatas.append({"filepath": entity.filepath, "type": "comment", "line": comment.start_line})
            
        # 3. Add Classes and Methods
        for cls in entity.classes:
            class_id = f"class:{cls.name}"
            self.graph_db.add_node(
                node_id=class_id,
                label="Class",
                properties={"name": cls.name, "filepath": entity.filepath}
            )
            self.graph_db.add_edge(file_id, class_id, "DECLARES_CLASS")
            
            for method in cls.methods:
                method_id = f"method:{cls.name}.{method.name}"
                self.graph_db.add_node(
                    node_id=method_id,
                    label="Method",
                    properties={"name": method.name, "signature": method.signature}
                )
                self.graph_db.add_edge(class_id, method_id, "HAS_METHOD")
                
                # Method calls
                for call in method.calls:
                    # In a fully resolved AST, we'd know the exact target class. 
                    # For now, we create a generic "call" edge to the method name.
                    target_id = f"method_name:{call}"
                    self.graph_db.add_node(target_id, label="MethodName", properties={"name": call})
                    self.graph_db.add_edge(method_id, target_id, "CALLS")
                    
                # If method has a docstring, add to vector DB
                if method.docstring:
                    doc_id = f"doc:{method_id}"
                    comment_ids.append(doc_id)
                    comment_texts.append(method.docstring)
                    comment_metadatas.append({"filepath": entity.filepath, "type": "docstring", "target": method_id})

        # 4. Add HTML Nodes
        for node in entity.html_nodes:
            node_id = f"html:{entity.filepath}:{node.start_line}:{node.tag}"
            if node.id_attr:
                node_id += f"#{node.id_attr}"
            
            self.graph_db.add_node(
                node_id=node_id,
                label=f"Html{node.node_type.capitalize()}",
                properties={"tag": node.tag, "id": node.id_attr, "class": node.class_attr}
            )
            rel_type = "HAS_INTERACTION" if node.node_type == "interaction" else "HAS_CONTAINER"
            self.graph_db.add_edge(file_id, node_id, rel_type)

        # 5. Add CSS Rules
        for rule in entity.css_rules:
            rule_id = f"css:{entity.filepath}:{rule.selector}"
            self.graph_db.add_node(
                node_id=rule_id,
                label="CssRule",
                properties={"selector": rule.selector}
            )
            self.graph_db.add_edge(file_id, rule_id, "DEFINES_STYLE")

        # 6. Add Imports
        for imp in entity.imports:
            # We don't always know if it's a script or stylesheet from the string alone,
            # but we can make an educated guess.
            imp_id = f"file:{imp}"
            self.graph_db.add_node(node_id=imp_id, label="File", properties={"filepath": imp})
            self.graph_db.add_edge(file_id, imp_id, "DEPENDS_ON")

        # Commit Graph
        self.graph_db.commit()
        
        # Commit Vectors
        if comment_ids:
            self.vector_db.add_texts(ids=comment_ids, texts=comment_texts, metadatas=comment_metadatas)
