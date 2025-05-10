from application.database.chromadb import ChromaDB
from typing import List, Dict, Any


class RAG:
    def __init__(self, collection_name: str = "test"):
        """
        Initialize RAG with ChromaDB client and collection.
        
        Args:
            collection_name (str): Name of the collection to use for document storage
        """
        self.client = ChromaDB()
        self.collection = self.client.get_collection(collection_name=collection_name)
    
    def query_similar_chunks(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        """
        Query the database for similar chunks based on the user prompt.
        
        Args:
            query (str): The user's query/prompt
            n_results (int): Number of similar chunks to retrieve (default: 3)
            
        Returns:
            List[Dict[str, Any]]: List of dictionaries containing similar chunks with their metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format the results
        similar_chunks = []
        for i in range(len(results["documents"][0])):
            chunk = {
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity_score": 1 - results["distances"][0][i]  # Convert distance to similarity score
            }
            similar_chunks.append(chunk)
            
        return similar_chunks
