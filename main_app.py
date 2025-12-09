# src/app/streamlit_app.py

import streamlit as st
from pathlib import Path
from text_handler.ocr_text import extract_text_from_pdf
from text_handler.structured_extractor import cleaned_text_extractor
from text_handler.text_splitter import get_chunks
from embeddings.chroma_store import create_chroma_from_docs, similarity_search_from_db


import json
import os
from langchain_core.documents import Document

if not os.path.exists("syllabus.json"):
    with open("syllabus.json", "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)


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

    # 1. Extrac the text from the file
    text = extract_text_from_pdf(file_path)

    # 2. Clean the text using LLM Google GEN AI
    cleaned_text = cleaned_text_extractor(text)
    text = None
    data_list = []
    try:
        with open("syllabus.json", "r", encoding="utf-8") as f:
            data_list = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        data_list = []

        data_list.append(cleaned_text)

    with open("syllabus.json", "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

    st.write("Saved successfully")

    # 3. Get the Chunks from the Cleaned Text
    chunks, meta_data = get_chunks(cleaned_text)
    cleaned_text = None

    # 4. Converting and adding Embedding to Chroma Cloud
    create_chroma_from_docs(chunks, meta_data)
    chunks = None
    meta_data = None


user_input = st.text_input("Type your question here...")

if user_input:
    st.write(user_input)

    results, json_output = similarity_search_from_db(user_input)
    st.json(json_output)
    # st.write(result)
