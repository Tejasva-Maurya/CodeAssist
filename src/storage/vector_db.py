import chromadb
from typing import List, Dict, Any

class VectorStorage:
    """
    Wrapper around ChromaDB for storing and semantic searching of 
    code chunks and comments.
    """
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        # We create a collection for code/comments
        self.collection = self.client.get_or_create_collection(
            name="codebase_embeddings",
            metadata={"hnsw:space": "cosine"}
        )

    def add_texts(self, ids: List[str], texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """
        Add texts to the vector database.
        ChromaDB uses its default embedding function (all-MiniLM-L6-v2) automatically if none provided.
        """
        if not texts:
            return
            
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )

    def delete_file_embeddings(self, filepath: str):
        """
        Surgically delete all embeddings associated with a specific file using metadata filtering.
        """
        self.collection.delete(where={"filepath": filepath})

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for the most relevant code chunks or comments based on semantic meaning.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        formatted_results = []
        if not results['ids']:
            return formatted_results
            
        # ChromaDB returns a list of lists for queries
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "id": results['ids'][0][i],
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                "distance": results['distances'][0][i] if 'distances' in results else None
            })
            
        return formatted_results
