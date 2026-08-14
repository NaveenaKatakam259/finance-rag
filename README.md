# 📈 Quarterly Financial Reports AI Assistant

A Retrieval-Augmented Generation (RAG) application built with **Streamlit**, **LangChain**, **ChromaDB**, and **Ollama (Llama 3.1)** that allows users to upload quarterly financial report PDFs and ask natural language questions about company financials.

The assistant retrieves relevant sections from uploaded reports and answers strictly based on the document content while providing source citations.

---

## 🚀 Features

- 📄 Upload multiple quarterly financial report PDFs
- 🔍 Automatically extract and chunk document text
- 🧠 Store document embeddings in ChromaDB
- 💬 Ask financial questions in natural language
- 📚 Retrieve relevant document chunks using semantic search
- 🤖 Generate answers using Ollama (Llama 3.1)
- 📌 Display source file names and page numbers
- 💾 Persistent local vector database

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Ollama
- Llama 3.1 (8B)
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers
- PyPDF
- python-dotenv

---

## 📂 Project Structure

```
finance-rag/
│
├── app.py                # Streamlit application
├── ingest.py             # PDF ingestion & indexing
├── rag.py                # Retrieval-Augmented Generation pipeline
├── data/                 # Uploaded PDF files
├── chroma_db/            # Persistent Chroma database
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/<your-github-username>/finance-rag.git

cd finance-rag
```

---

### Create Virtual Environment

Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download from

https://ollama.com/download

Pull the Llama model

```bash
ollama pull llama3.1:8b
```

Start Ollama

```bash
ollama serve
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## How It Works

1. Upload one or more quarterly financial report PDFs.
2. Click **Index Documents**.
3. Text is extracted from PDFs.
4. Documents are split into chunks.
5. Chunks are converted into embeddings using HuggingFace.
6. Embeddings are stored in ChromaDB.
7. User asks a financial question.
8. Relevant chunks are retrieved.
9. Ollama (Llama 3.1) generates an answer using only retrieved context.
10. Sources and page numbers are displayed for verification.

---

## Example Questions

- What was Apple's total revenue in Q1?
- Compare Q1 and Q2 revenue.
- What were Services revenues in Q3?
- How much operating income was reported?
- What were the net sales by product category?
- Compare gross margins across quarters.
- What risks were mentioned in the quarterly report?
- Summarize the financial highlights.

---

## Screenshots

(Add screenshots here)

---

## Future Improvements

- Multi-company comparison
- Financial trend visualization
- Charts and dashboards
- Hybrid Search (BM25 + Vector Search)
- OCR support for scanned PDFs
- Conversation memory
- Support for additional LLMs

---

## Author

**Naveena Katakam**

B.Tech Information Technology

AI & Software Development Enthusiast

---

## License

This project is developed for educational purposes.