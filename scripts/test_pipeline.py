import sys
import os
import json

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from extractor.java import JavaExtractor
from storage.sqlite_graph import SQLiteStorage
from storage.vector_db import VectorStorage
from pipeline.loader import PipelineLoader

def main():
    target_file = os.path.join(os.path.dirname(__file__), '..', 'tests', 'Dummy.java')
    
    codeassist_dir = os.path.join(os.path.dirname(__file__), '..', '.codeassist')
    os.makedirs(codeassist_dir, exist_ok=True)
    db_path = os.path.join(codeassist_dir, 'code_graph.db')
    chroma_path = os.path.join(codeassist_dir, 'chroma_db')
    
    with open(target_file, 'rb') as f:
        content = f.read()
        
    print("1. Extracting data...")
    extractor = JavaExtractor()
    file_entity = extractor.parse_file(target_file, content)
    
    print("2. Loading into Data Warehouse...")
    graph_db = SQLiteStorage(db_path)
    vector_db = VectorStorage(chroma_path)
    loader = PipelineLoader(graph_db, vector_db)
    
    loader.load_file_entity(file_entity)
    print("Data loaded successfully!")
    
    print("\n--- Verifying Graph DB ---")
    file_id = f"file:{target_file}"
    edges = graph_db.get_edges(file_id, direction="out")
    print(f"Edges connected to {file_id}:")
    for edge in edges:
        print(f"  -> [{edge['relationship_type']}] {edge['target_id']}")
        
    print("\n--- Verifying Vector DB ---")
    query = "testing the extractor"
    print(f"Semantic search for: '{query}'")
    results = vector_db.search(query, n_results=1)
    if results:
        for res in results:
            print(f"  Found: {res['text']} (Distance: {res['distance']})")
    else:
        print("  No results found.")

if __name__ == "__main__":
    main()
