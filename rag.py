import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

CHROMA_PATH = "chroma_db"

PROMPT_TEMPLATE = """
You are a strict, factual Financial Analyst AI Assistant.
Answer the user's question using ONLY the provided context below.

If the context does not contain the information needed to answer the question, 
you must reply exactly with: "The requested information is not available in the uploaded documents."
Do not guess, speculate, or use outside knowledge.

When providing facts, cite the source filename and page number inline using this format: [Source: <filename>, Page: <page_number>].

Context:
{context}

Question:
{question}

Answer:
"""

def format_docs(docs):
    formatted_chunks = []
    for doc in docs:
        source = os.path.basename(doc.metadata.get("source", "Unknown"))
        page = doc.metadata.get("page", 0) + 1 
        text = doc.page_content
        formatted_chunks.append(f"[Source: {source}, Page: {page}]\n{text}")
    return "\n\n".join(formatted_chunks)

def get_answer(question: str):
    if not os.path.exists(CHROMA_PATH):
        return "Error: Database not found. Please upload documents and index them first.", []

  
    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = Chroma(
        persist_directory=CHROMA_PATH,
          embedding_function=embeddings
          )
    
    retriever = db.as_retriever(search_kwargs={"k": 5})
    
  
    llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
     )
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    docs = retriever.invoke(question)
    context_string = format_docs(docs)
    
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({
        "context": context_string, 
        "question": question
    })
    
    return answer, docs