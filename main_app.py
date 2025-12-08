# src/app/streamlit_app.py

import streamlit as st
from pathlib import Path
from text_handler.ocr_text import extract_text_from_pdf
from text_handler.structured_extractor import cleaned_text_extractor
from embeddings.embedder import get_embedding
from embeddings.chroma_store import create_chroma_from_docs


import json
from langchain_core.documents import Document

# Set page config
st.set_page_config(page_title="Syllabus RAG App", page_icon="📚", layout="wide")

# Title
st.title("📚 EduRAG Application")
st.markdown(
    """
    Upload your syllabus PDFs and interact with the chatbot to generate questions
    and get feedback on answers.
    """
)

# --- Sidebar: File Upload ---
st.sidebar.header("Upload PDFs")
uploaded_files = st.sidebar.file_uploader(
    "Upload syllabus PDFs", accept_multiple_files=True, type=["pdf"]
)

# Directory to store PDFs temporarily
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Store uploaded files
uploaded_file_paths = []
if uploaded_files:
    for file in uploaded_files:
        file_path = DATA_DIR / file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        uploaded_file_paths.append(file_path)
    st.sidebar.success(f"Uploaded {len(uploaded_file_paths)} files successfully!")

# --- Main: Chat Interface ---
st.subheader("💬 Chat with EduRAG")
chat_placeholder = st.empty()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Getting the text from the PDF files
for file_path in uploaded_file_paths:
    text = extract_text_from_pdf(file_path)
    with open("text.txt", "w") as f:
        f.write(text)
    cleaned_text = cleaned_text_extractor(text)
    st.write(cleaned_text)
    with open("syllabus.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_text, f, ensure_ascii=False, indent=4)


# Chat input
user_input = st.text_input("Type your question here...")

if user_input:
    # Placeholder bot response (will be replaced by actual RAG LLM)
    bot_response = "This is a placeholder response. Once embeddings are ready, real answers will appear."

    # Update chat history
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    st.session_state.chat_history.append({"role": "bot", "message": bot_response})
