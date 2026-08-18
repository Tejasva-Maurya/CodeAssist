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
    
    # 1. Get existing file metadata
    existing_files = graph_db.get_all_file_metadata()
    current_files = {}
    
    # 2. Walk directory to find current files and their mtime
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SUPPORTED_EXTENSIONS:
                filepath = os.path.join(root, file)
                mtime = os.path.getmtime(filepath)
                current_files[filepath] = mtime
                
    # 3. Determine Deltas (New, Modified, Unchanged, Deleted)
    new_files = []
    modified_files = []
    deleted_files = []
    unchanged_count = 0
    
    for filepath, mtime in current_files.items():
        if filepath not in existing_files:
            new_files.append(filepath)
        elif mtime > existing_files[filepath]:
            modified_files.append(filepath)
        else:
            unchanged_count += 1
            
    for filepath in existing_files.keys():
        if filepath not in current_files:
            deleted_files.append(filepath)
            
    print(f"Delta Analysis Complete:")
    print(f"  - Unchanged: {unchanged_count}")
    print(f"  - New:       {len(new_files)}")
    print(f"  - Modified:  {len(modified_files)}")
    print(f"  - Deleted:   {len(deleted_files)}")
    
    # 4. Erase Orphaned/Modified data before re-indexing
    files_to_erase = deleted_files + modified_files
    if files_to_erase:
        print(f"Erasing old data for {len(files_to_erase)} files...")
        for filepath in tqdm(files_to_erase, desc="Erasing"):
            graph_db.delete_file_data(filepath)
            vector_db.delete_file_embeddings(filepath)
        graph_db.commit()

    files_to_process = new_files + modified_files
    if not files_to_process:
        print("\nKnowledge base is already up-to-date!")
        return

    # 5. Extract and Load
    successful = 0
    failed = 0
    
    print(f"Beginning extraction for {len(files_to_process)} files...")
    for filepath in tqdm(files_to_process, desc="Indexing"):
        try:
            extractor = get_extractor(filepath)
            with open(filepath, 'rb') as f:
                content = f.read()
            entity = extractor.parse_file(filepath, content)
            loader.load_file_entity(entity)
            graph_db.upsert_file_metadata(filepath, current_files[filepath])
            successful += 1
        except Exception as e:
            # print(f"Error processing {filepath}: {e}")
            failed += 1
            
    graph_db.commit()
            
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
