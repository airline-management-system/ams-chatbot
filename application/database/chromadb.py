from application.config import Config
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from typing import Any


class ChromaDB:
    __client: chromadb.PersistentClient

    def __init__(self):
        """Initialize a new ChromaDB client with persistent storage."""
        self.__client = chromadb.PersistentClient()
        # Initialize genai client for embeddings
        self.google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=Config.API_KEY)
    
    def get_client(self) -> chromadb.PersistentClient:
        """Returns the ChromaDB persistent client instance."""
        return self.__client
    
    def get_collection(self,collection_name:str) -> Any:
        """
        Retrieves an existing collection from ChromaDB.
        
        Args:
            collection_name (str): Name of the collection to retrieve
            
        Returns:
            Any: The collection if found, None if there's an error
        """
        try:
            collection = self.__client.get_collection(
                name=collection_name,
                embedding_function=self.google_ef
            )
            return collection
        except chromadb.errors.InternalError as e:
            print(f"Error getting collection: {e}")
            return None
    
    def create_collection(self,collection_name:str) -> Any:
        """
        Creates a new collection in ChromaDB.
        
        Args:
            collection_name (str): Name of the collection to create
            
        Returns:
            Any: The newly created collection if successful, None if there's an error
        """
        try:
            # Create new collection if it doesn't exist
            collection = self.__client.create_collection(
                name=collection_name,
                embedding_function=self.google_ef
            )
            return collection
        except chromadb.errors.InternalError as e:
            print(f"Error creating collection:{e}")
            return None
            
        
    def add_document(self, collection, chunks:list[Document]):
        """
        Adds or updates documents in a ChromaDB collection.
        
        Args:
            collection: The ChromaDB collection to add documents to
            chunks (list[Document]): List of Document objects containing the content and metadata to add
        """
        # Prepare the data for ChromaDB
        documents = [chunk.page_content for chunk in chunks]  # List of strings
        metadatas = [chunk.metadata for chunk in chunks]      # List of dictionaries
        ids = [f"id{i}" for i in range(len(chunks))]          # List of string IDs

        # Add chunks to the collection
        try:
            collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"Saved {len(chunks)} chunks to {Config.CHROMA_PATH}.")
        except Exception as e:
            print(f"Error adding documents: {e}")