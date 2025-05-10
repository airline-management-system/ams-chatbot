from application.config import Config
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from application.database.chromadb import ChromaDB


# Create chromadb client
chroma_client = ChromaDB()

def main():
    documents = load_documents()
    chunks = split_text(documents)
    collection_name = 'test'
    
    collection = chroma_client.create_collection(collection_name=collection_name)
    if collection is None:
        collection = chroma_client.get_collection(collection_name=collection_name)
    
    chroma_client.add_document(collection=collection, chunks=chunks)


def load_documents():
    data_dir = Config.DATA_PATH
    
    # Load PDF files in the directory
    loader = DirectoryLoader(
        data_dir,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
        separators=["\n\n", "\n", ".", " ", ""],  # prioritize on paragraph or sentence end
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


if __name__ == "__main__":
    main()