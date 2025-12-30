from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from ingest import load_and_chunk_pdfs
import os

# We don't need the OpenAI API key anymore! You can remove that line.
# We are using a FREE model from Hugging Face.

def create_vector_store():
    # 1. Load and chunk the PDFs
    chunks = load_and_chunk_pdfs()
    if not chunks:
        return None

    # 2. Create the FREE embedding function
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 3. Create and persist the vector database
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function,
        persist_directory="./chroma_db"  # Folder where the knowledge base will be stored
    )
    vector_db.persist()
    print("Vector DB created and persisted at './chroma_db' using FREE Hugging Face embeddings!")
    return vector_db

if __name__ == "__main__":
    create_vector_store()