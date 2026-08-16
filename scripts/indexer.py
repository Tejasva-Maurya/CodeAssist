import sys
import os
import argparse
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from extractor import get_extractor
from storage.sqlite_graph import SQLiteStorage
from storage.vector_db import VectorStorage
from pipeline.loader import PipelineLoader

SUPPORTED_EXTENSIONS = {'.java', '.cs', '.html', '.htm', '.css'}
IGNORE_DIRS = {'.git', 'node_modules', 'venv', '.venv', 'dist', 'build', '.codeassist'}

def build_index(repo_path: str):
    print(f"Initializing Data Warehouse for {repo_path}...")
    
    codeassist_dir = os.path.join(repo_path, '.codeassist')
    os.makedirs(codeassist_dir, exist_ok=True)
    db_path = os.path.join(codeassist_dir, 'code_graph.db')
    chroma_path = os.path.join(codeassist_dir, 'chroma_db')
    
    graph_db = SQLiteStorage(db_path)
    vector_db = VectorStorage(chroma_path)
    loader = PipelineLoader(graph_db, vector_db)
    
    files_to_process = []
    
    # 1. Walk directory
    for root, dirs, files in os.walk(repo_path):
        # Ignore hidden or build dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                files_to_process.append(os.path.join(root, file))
                
    print(f"Found {len(files_to_process)} supported files. Beginning extraction...")
    
    # 2. Extract and Load
    successful = 0
    failed = 0
    
    for filepath in tqdm(files_to_process, desc="Indexing"):
        try:
            extractor = get_extractor(filepath)
            with open(filepath, 'rb') as f:
                content = f.read()
            entity = extractor.parse_file(filepath, content)
            loader.load_file_entity(entity)
            successful += 1
        except Exception as e:
            # print(f"Error processing {filepath}: {e}")
            failed += 1
            
    print("\nIndexing Complete!")
    print(f"Successfully Indexed: {successful} files")
    if failed > 0:
        print(f"Failed to Index: {failed} files")
    print(f"Data stored securely in {codeassist_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codebase Reverse Engineering Indexer")
    parser.add_argument("repo_path", help="Path to the repository you want to index")
    args = parser.parse_args()
    
    target_repo = os.path.abspath(args.repo_path)
    if not os.path.isdir(target_repo):
        print(f"Error: Directory '{target_repo}' does not exist.")
        sys.exit(1)
        
    build_index(target_repo)
