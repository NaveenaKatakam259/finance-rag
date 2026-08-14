import os
import shutil
import chromadb
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

DATA_DIR = "data"
CHROMA_PATH = "chroma_db"

def process_pdfs(data_dir: str = DATA_DIR, chroma_path: str = CHROMA_PATH):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith(".pdf")]
    if not pdf_files:
        return 0, 0

    all_documents = []
    for file_name in pdf_files:
        file_path = os.path.join(data_dir, file_name)
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        all_documents.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(all_documents)


    chromadb.api.client.SharedSystemClient.clear_system_cache()
    
    if os.path.exists(chroma_path):
        shutil.rmtree(chroma_path)

  
    embeddings = HuggingFaceEmbeddings(
     model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path
    )

    return len(pdf_files), len(chunks)

if __name__ == "__main__":
    print("Starting ingestion pipeline...")
    files_count, chunks_count = process_pdfs()
    print(f"✅ Ingestion complete. {files_count} files processed, {chunks_count} chunks stored.")