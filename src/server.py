import asyncio
import os
import sys
from fastmcp import FastMCP
from typing import List, Dict, Any

# Add src to path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from storage.sqlite_graph import SQLiteStorage
from storage.vector_db import VectorStorage

# Initialize MCP Server
mcp = FastMCP("Codebase Reverse Engineering Engine")

# Determine Target Repo Root (Default to current working directory if not provided)
TARGET_REPO = os.environ.get("TARGET_REPO", os.getcwd())
CODEASSIST_DIR = os.path.join(TARGET_REPO, ".codeassist")
os.makedirs(CODEASSIST_DIR, exist_ok=True)

# Initialize Databases inside the target repo
db_path = os.path.join(CODEASSIST_DIR, 'code_graph.db')
chroma_path = os.path.join(CODEASSIST_DIR, 'chroma_db')

graph_db = SQLiteStorage(db_path)
vector_db = VectorStorage(chroma_path)

@mcp.tool()
def query_architecture_graph(node_id: str, direction: str = "both") -> List[Dict[str, Any]]:
    """
    Query the graph database to find relationships for a specific node.
    node_id examples: 'file:/path/to/file', 'class:MyClass', 'method:MyClass.myMethod'
    direction: 'out', 'in', or 'both'
    """
    edges = graph_db.get_edges(node_id, direction)
    return edges

@mcp.tool()
def semantic_code_search(query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a semantic search across the codebase docstrings and comments.
    Returns the most relevant code chunks matching the meaning of the query.
    """
    results = vector_db.search(query, n_results=n_results)
    return results

@mcp.tool()
def get_node_details(node_id: str) -> Dict[str, Any]:
    """
    Retrieve all properties of a specific node (e.g., to get the signature of a method).
    """
    node = graph_db.get_node(node_id)
    if not node:
        return {"error": f"Node {node_id} not found."}
    return node

@mcp.tool()
def get_source_code(file_path: str) -> Dict[str, Any]:
    """
    Read the raw text content of a source code file.
    Use this to read the actual implementation (method bodies, state machines) of core Domain entities or Command Handlers when AST metadata is insufficient.
    file_path should be a relative path from the target repository root (or absolute).
    """
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.join(TARGET_REPO, file_path)
            
        if os.path.isdir(file_path):
            return {"error": f"Path is a directory, not a file: {file_path}. Please provide a path to a specific file."}
            
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return {"file_path": file_path, "content": content}
    except Exception as e:
        return {"error": f"Failed to read source code: {str(e)}"}

@mcp.tool()
def get_project_context() -> Dict[str, Any]:
    """
    Retrieve the global configuration files and project context (like pom.xml, package.json, AppHost/Program.cs).
    Use this to definitively identify the infrastructure, framework versions, and databases used by the repository.
    """
    import pathlib
    import re
    from language_registry import PARSERS
    
    context = {}
    found_files = {}
    dependencies = set()
    frameworks = set()
    
    repo_path = pathlib.Path(TARGET_REPO)
    
    for parser in PARSERS:
        for pattern in parser.get_patterns():
            matches = list(repo_path.rglob(pattern.replace("**/", "")))
            matches.sort()
            
            count = 0
            for match in matches:
                path_str = str(match)
                if any(ignore in path_str for ignore in ["node_modules", "bin" + os.sep, "obj" + os.sep, "target" + os.sep, "venv", ".git"]):
                    continue
                    
                try:
                    with open(match, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    rel_path = os.path.relpath(match, TARGET_REPO)
                    
                    if parser.is_manifest(path_str):
                        parser.parse(path_str, content, dependencies, frameworks)
                    else:
                        if count >= 5:
                            continue
                        if len(content) > 10000:
                            content = content[:10000] + "... [TRUNCATED]"
                        found_files[rel_path] = content
                        count += 1
                except Exception:
                    pass
                
    context["configuration_files"] = found_files
    if dependencies:
        context["extracted_dependencies"] = sorted(list(dependencies))
    if frameworks:
        context["extracted_frameworks"] = sorted(list(frameworks))
        
    return context

import glob

# Dynamically expose all skills in the skills/ directory as MCP Prompts
SKILLS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'skills')

def register_prompts():
    if not os.path.isdir(SKILLS_DIR):
        return

    for skill_file in glob.glob(os.path.join(SKILLS_DIR, "*.md")):
        skill_name = os.path.splitext(os.path.basename(skill_file))[0]
        
        def make_handler(filepath):
            def handler() -> list:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                return [content]
            
            # FastMCP uses the function name if name isn't provided, 
            # but we provide it explicitly anyway.
            handler.__name__ = f"prompt_{skill_name}"
            return handler
            
        mcp.prompt(name=skill_name, description=f"Execute the {skill_name} reverse engineering skill.")(make_handler(skill_file))

register_prompts()

if __name__ == "__main__":
    # Run the server over stdio
    mcp.run()
