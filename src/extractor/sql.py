import sqlglot
from sqlglot import exp
import re
from typing import Optional

from .base import BaseExtractor, FileEntity, ClassEntity, MethodEntity

class SqlExtractor(BaseExtractor):
    """
    Extracts structural metadata from SQL files using a Hybrid approach.
    It attempts to parse the AST using sqlglot, and gracefully falls back to Regex
    if proprietary dialect syntax causes a parsing exception.
    """
    def __init__(self):
        super().__init__("sql")

    def parse_file(self, filepath: str, content: bytes) -> FileEntity:
        text = content.decode('utf-8', errors='ignore')
        
        entity = FileEntity(filepath=filepath, language="sql")
        
        # We create a dummy "Schema" container to hold standalone procedures/functions
        global_schema = ClassEntity(
            name="DatabaseSchema",
            type="DatabaseSchema",
            start_line=1,
            end_line=len(text.splitlines())
        )
        
        try:
            # Parse multiple dialects generously by reading generically
            parsed_statements = sqlglot.parse(text)
            
            for stmt in parsed_statements:
                if not stmt:
                    continue
                    
                if isinstance(stmt, exp.Create):
                    kind = stmt.args.get("kind", "")
                    if type(kind) is str:
                        kind = kind.upper()
                    else:
                        kind = str(kind).upper()
                        
                    if "TABLE" in kind or "VIEW" in kind:
                        name = stmt.this.sql().replace('"', '').replace('`', '')
                        cls = ClassEntity(
                            name=name,
                            type="DatabaseTable" if "TABLE" in kind else "DatabaseView",
                            start_line=1,
                            end_line=1,
                            docstring=stmt.sql() # The full DDL is stored as the docstring for Vector Semantic Search
                        )
                        entity.classes.append(cls)
                        
                    elif "PROCEDURE" in kind or "FUNCTION" in kind or "PROC" in kind:
                        name = stmt.this.sql().replace('"', '').replace('`', '')
                        method = MethodEntity(
                            name=name,
                            type="StoredProcedure" if "PROC" in kind else "DatabaseFunction",
                            signature=name,
                            start_line=1,
                            end_line=1,
                            docstring=stmt.sql() # The body of the proc is vectorized
                        )
                        global_schema.methods.append(method)

        except Exception as e:
            # Graceful Fallback: Robust Regex for proprietary extensions
            self._regex_fallback(text, entity, global_schema)
            
        if global_schema.methods:
            entity.classes.append(global_schema)
            
        return entity
        
    def _regex_fallback(self, text: str, entity: FileEntity, global_schema: ClassEntity):
        # Regex to find Tables and Views
        for match in re.finditer(r"(?i)CREATE\s+(TABLE|VIEW)\s+([a-zA-Z0-9_\[\]\.]+)", text):
            kind = match.group(1).upper()
            name = match.group(2).strip("[]")
            cls = ClassEntity(
                name=name,
                type="DatabaseTable" if kind == "TABLE" else "DatabaseView",
                start_line=1,
                end_line=1,
                docstring=text[:5000] # Cap text to avoid massive duplication in dumps
            )
            entity.classes.append(cls)
            
        # Regex to find Procedures and Functions
        for match in re.finditer(r"(?i)CREATE\s+(PROCEDURE|FUNCTION|PROC)\s+([a-zA-Z0-9_\[\]\.]+)", text):
            kind = match.group(1).upper()
            name = match.group(2).strip("[]")
            method = MethodEntity(
                name=name,
                type="StoredProcedure" if "PROC" in kind else "DatabaseFunction",
                signature=name,
                start_line=1,
                end_line=1,
                docstring=text[:5000]
            )
            global_schema.methods.append(method)
