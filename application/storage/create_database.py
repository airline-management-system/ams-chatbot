from application.config import Config
from langchain_community.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from typing import Any


CHROMA_PATH = "chroma"
DATA_PATH = "./data/flights.json"

# Initialize genai client for embeddings
google_ef = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=Config.API_KEY)


class ChromaDB:
    __client: chromadb.PersistentClient

    def __init__(self):
        self.__client = chromadb.PersistentClient()
    
    def get_client(self) -> chromadb.PersistentClient:
        return self.__client
    
    def get_collection(self,collection_name:str) -> Any:
        try:
            collection = self.__client.get_collection(
                name=collection_name,
                embedding_function=google_ef
            )
            return collection
        except chromadb.errors.InternalError as e:
            print(f"Error getting collection: {e}")
            return None
    
    def create_collection(self,collection_name:str) -> Any:
        try:
            # Create new collection if it doesn't exist
            collection = self.__client.create_collection(
                name=collection_name,
                embedding_function=google_ef
            )
            return collection
        except chromadb.errors.InternalError as e:
            print(f"Error creating collection:{e}")
            return None
            
        
    def add_document(self, collection, chunks:list[Document]):
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
            print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
        except Exception as e:
            print(f"Error adding documents: {e}")


# Create chromadb client
chroma_client = ChromaDB()

def main():

    documents = load_documents()
    chunks = split_text(documents)
    collection_name = 'test-rag'
    
    collection = chroma_client.create_collection(collection_name=collection_name)
    if collection is None:
        collection = chroma_client.get_collection(collection_name=collection_name)
    
    chroma_client.add_document(collection=collection, chunks=chunks)


def load_documents():
    loader = JSONLoader(
        file_path=DATA_PATH, 
        jq_schema='.[] | "Flight \(.flight_number) from \(.departure_airport) to \(.arrival_airport) departs at \(.departure_time) on \(.aircraft_type)"',
        text_content=False
    )
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


if __name__ == "__main__":
    main()