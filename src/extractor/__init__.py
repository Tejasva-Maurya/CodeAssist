from .base import BaseExtractor, FileEntity, ClassEntity, MethodEntity, CommentEntity
from .java import JavaExtractor
from .c_sharp import CSharpExtractor
from .html import HtmlExtractor
from .css import CssExtractor
from .sql import SqlExtractor

def get_extractor(filepath: str) -> BaseExtractor:
    if filepath.endswith(".java"):
        return JavaExtractor()
    elif filepath.endswith(".cs"):
        return CSharpExtractor()
    elif filepath.endswith(".html") or filepath.endswith(".htm"):
        return HtmlExtractor()
    elif filepath.endswith(".css"):
        return CssExtractor()
    elif filepath.endswith(".sql"):
        return SqlExtractor()
    else:
        raise ValueError(f"No extractor found for {filepath}")

__all__ = [
    "get_extractor",
    "BaseExtractor",
    "FileEntity",
    "ClassEntity",
    "MethodEntity",
    "CommentEntity",
    "JavaExtractor",
    "CSharpExtractor",
    "HtmlExtractor",
    "CssExtractor",
    "SqlExtractor"
]
