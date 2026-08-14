import streamlit as st
import os

st.set_page_config(page_title="Quarterly Financial Reports AI Assistant", page_icon="📈", layout="wide")

st.title("📈 Quarterly Financial Reports")
st.markdown("Upload quarterly result PDFs, index them into ChromaDB, and query financial metrics with citations.")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


with st.sidebar:
    st.header("1. Document Management")
    uploaded_files = st.file_uploader(
        "Upload Quarterly Result PDFs", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    if st.button("Index Documents", type="primary"):
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_path = os.path.join(DATA_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            with st.spinner("Processing PDFs, chunking text, and saving embeddings..."):
                from ingest import process_pdfs
                files_count, chunks_count = process_pdfs()
                st.success(f"✅ {files_count} files processed, {chunks_count} chunks stored in ChromaDB.")
        else:
            st.warning("Please upload at least one PDF file first.")

    st.markdown("---")
    st.header("2. System Status")
    if os.path.exists("chroma_db"):
        st.success("✅ Knowledge Base Active (Persisted on Disk)")
    else:
        st.info("ℹ️ No active vector store. Upload PDFs and click 'Index Documents'.")
        
    st.markdown("---")
    st.markdown("**Model:** `llama3.1:8b (Ollama)`")
    st.markdown("**Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`")
    st.markdown("**Vector DB:** `ChromaDB`")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("View Verified Source Context"):
                for i, doc in enumerate(message["sources"]):
                    filename = os.path.basename(doc.metadata.get('source', 'Unknown'))
                    page = doc.metadata.get('page', 0) + 1
                    st.markdown(f"**Chunk {i+1} | Source: {filename} | Page: {page}**")
                    st.caption(doc.page_content)
                    st.markdown("---")

if user_query := st.chat_input("E.g., What was total revenue in the most recent quarter?"):
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    from rag import get_answer
    with st.chat_message("assistant"):
        with st.spinner("Searching financial reports..."):
            answer, sources = get_answer(user_query)
            st.markdown(answer)
            
            if sources:
                with st.expander("View Verified Source Context"):
                    for i, doc in enumerate(sources):
                        filename = os.path.basename(doc.metadata.get('source', 'Unknown'))
                        page = doc.metadata.get('page', 0) + 1
                        st.markdown(f"**Chunk {i+1} | Source: {filename} | Page: {page}**")
                        st.caption(doc.page_content)
                        st.markdown("---")

    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer,
        "sources": sources
    })
