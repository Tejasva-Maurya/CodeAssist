from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# --- Data Models ---

class CommentEntity(BaseModel):
    text: str
    start_line: int
    end_line: int

class MethodEntity(BaseModel):
    name: str
    signature: str
    start_line: int
    end_line: int
    docstring: Optional[str] = None
    calls: List[str] = [] # List of method names this method calls

class ClassEntity(BaseModel):
    name: str
    start_line: int
    end_line: int
    methods: List[MethodEntity] = []
    docstring: Optional[str] = None
    superclasses: List[str] = []

class HtmlNodeEntity(BaseModel):
    tag: str
    id_attr: Optional[str] = None
    class_attr: Optional[str] = None
    node_type: str  # e.g., 'interaction', 'container'
    start_line: int
    end_line: int

class CssRuleEntity(BaseModel):
    selector: str
    start_line: int
    end_line: int

class FileEntity(BaseModel):
    filepath: str
    classes: List[ClassEntity] = []       # For OOP languages
    html_nodes: List[HtmlNodeEntity] = [] # For HTML
    css_rules: List[CssRuleEntity] = []   # For CSS
    imports: List[str] = []               # includes <script src="...">, <link href="...">, @import
    comments: List[CommentEntity] = []

# --- Base Extractor Interface ---

class BaseExtractor(ABC):
    """
    Abstract base class for all language-specific extractors.
    It parses source code and returns a standardized FileEntity.
    """
    
    def __init__(self, language_name: str):
        self.language_name = language_name

    @abstractmethod
    def parse_file(self, filepath: str, content: bytes) -> FileEntity:
        """
        Parse the file content and extract all relevant entities (Classes, Methods, Imports, Comments).
        """
        pass
