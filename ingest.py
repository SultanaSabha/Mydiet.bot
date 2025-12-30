from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_and_chunk_pdfs(pdf_directory="./data"):
    documents = []
    
    # Check if the data directory exists
    if not os.path.exists(pdf_directory):
        print(f"Error: Directory '{pdf_directory}' not found. Please create a 'data' folder with PDFs.")
        return None

    # Load each PDF in the data directory
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            print(f"Loading {pdf_file}...")
            try:
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")

    if not documents:
        print("No PDFs found or all PDFs failed to load.")
        return None

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Successfully loaded and split into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    chunks = load_and_chunk_pdfs()
    if chunks:
        print(f"First chunk preview: {chunks[0].page_content[:200]}...")  # Show first 200 chars