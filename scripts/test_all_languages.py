import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from extractor import get_extractor
from storage.sqlite_graph import SQLiteStorage
from storage.vector_db import VectorStorage
from pipeline.loader import PipelineLoader

def process_file(filepath: str, loader: PipelineLoader):
    print(f"Processing {filepath}...")
    try:
        extractor = get_extractor(filepath)
        with open(filepath, 'rb') as f:
            content = f.read()
        entity = extractor.parse_file(filepath, content)
        loader.load_file_entity(entity)
        print(f"  -> Extracted and loaded successfully.")
    except Exception as e:
        print(f"  -> Failed: {e}")

if __name__ == "__main__":
    codeassist_dir = os.path.join(os.path.dirname(__file__), '..', '.codeassist')
    os.makedirs(codeassist_dir, exist_ok=True)
    db_path = os.path.join(codeassist_dir, 'code_graph.db')
    chroma_path = os.path.join(codeassist_dir, 'chroma_db')
    
    graph_db = SQLiteStorage(db_path)
    vector_db = VectorStorage(chroma_path)
    loader = PipelineLoader(graph_db, vector_db)
    
    test_files = [
        os.path.join(os.path.dirname(__file__), '..', 'tests', 'Login.cs'),
        os.path.join(os.path.dirname(__file__), '..', 'tests', 'index.html'),
        os.path.join(os.path.dirname(__file__), '..', 'tests', 'style.css')
    ]
    
    for f in test_files:
        process_file(f, loader)
        
    print("\n--- Verifying HTML Nodes in Graph ---")
    file_id = f"file:{test_files[1]}"
    edges = graph_db.get_edges(file_id, "out")
    for edge in edges:
        if edge['relationship_type'] in ('HAS_INTERACTION', 'HAS_CONTAINER', 'DEPENDS_ON'):
            print(f"[{edge['relationship_type']}] -> {edge['target_id']}")
