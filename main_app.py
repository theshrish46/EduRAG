import streamlit as st
from pathlib import Path
import os
import json

# --- Custom Imports ---
from text_handler.ocr_text import extract_text_from_pdf
from text_handler.structured_extractor import cleaned_text_extractor
from text_handler.text_splitter import get_chunks
from embeddings.chroma_store import (
    create_chroma_from_docs,
    similarity_search_from_db,
    check_file_exists,
)


# Ensure your folder is named 'generation'
from generator.question_generator import generate_questions_chain
from grading.grader import grade_answer_image

# NEW IMPORT for PDF
from utils.pdf_utils import generate_pdf_from_questions

# --- Page Configuration ---
st.set_page_config(page_title="Syllabus RAG App", page_icon="📚", layout="wide")

st.title("📚 EduRAG Application")

# --- State Management ---
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# Initialize session state for the PDF to persist after button click
if "generated_pdf" not in st.session_state:
    st.session_state.generated_pdf = None

# --- Sidebar: File Upload ---
st.sidebar.header("Upload PDFs")
uploaded_files = st.sidebar.file_uploader(
    "Upload syllabus PDFs", accept_multiple_files=True, type=["pdf"]
)

st.sidebar.header("Select Format")

format_type = st.sidebar.radio(
    "Choose Assessment Type",
    ("FA Internals (Max Marks 30)", "SA Externals (Max Marks 100)"),
)

st.sidebar.header("Adjust Temperature")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.1)

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def process_pdf(file):
    try:
        file_path = DATA_DIR / file.name
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        text = extract_text_from_pdf(file_path)
        cleaned_text = cleaned_text_extractor(text)
        chunks, meta_data = get_chunks(cleaned_text, filename=file.name)
        create_chroma_from_docs(chunks, meta_data)
        return True
    except Exception as e:
        st.error(f"Error processing {file.name}: {str(e)}")
        return False


# --- Main Logic: Handle File Uploads ---
if uploaded_files:
    new_files_count = 0
    for file in uploaded_files:
        if file.name in st.session_state.processed_files:
            continue
        if check_file_exists(file.name):
            st.sidebar.warning(
                f"File '{file.name}' is already in the Database. Skipping."
            )
            st.session_state.processed_files.add(file.name)
            continue

        with st.spinner(f"Processing {file.name}..."):
            success = process_pdf(file)
            if success:
                st.session_state.processed_files.add(file.name)
                new_files_count += 1

    if new_files_count > 0:
        st.sidebar.success(f"Successfully processed {new_files_count} new file(s)!")

# --- SECTION 1: Context Search (Optional Debugging) ---
st.divider()
with st.expander("🔍 Debug: Search Syllabus Context"):
    user_input = st.text_input("Search for a topic in your syllabus...")
    if user_input:
        results, json_output = similarity_search_from_db(user_input)
        st.json(json_output)


# --- SECTION 2: PDF Question Generator ---
st.divider()
st.subheader("📝 Question Paper Generator (PDF)")

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("Enter Subject Name")
    topic_input = st.text_input("Enter Topic (e.g., 'Module 5')")

with col2:
    blooms_level = st.multiselect(
        "Select Bloom's Taxonomy Level",
        [
            "L1 - Remember",
            "L2 - Understand",
            "L3 - Apply",
            "L4 - Analyze",
            "L5 - Evaluate",
            "L6 - Create",
        ],
    )


# Button to Trigger Generation
if st.button("Generate Question Paper"):
    if not subject or not topic_input:
        st.warning("Please fill in both Subject and Topic.")
    else:
        st.session_state.generated_pdf = None  # Reset previous state

        with st.spinner(f"Creating Questions for {topic_input}..."):
            # 1. Get output from the LangChain chain
            generated_data = generate_questions_chain(
                subject, topic_input, blooms_level, format_type, temperature
            )

            if isinstance(generated_data, list):
                pdf_bytes = generate_pdf_from_questions(
                    questions_json=generated_data,
                    subject=subject if subject else topic_input,
                    blooms_level=[b.split("-")[0].strip() for b in blooms_level],
                    max_marks=(
                        30 if format_type == "FA Internals (Max Marks 30)" else 100
                    ),
                )

                st.session_state.generated_pdf = pdf_bytes
                st.success("Question generated successfully!")
            else:
                st.error(
                    "The generator returned no data. Check your API connection or Context."
                )

if st.session_state.generated_pdf:
    st.download_button(
        label="Download PDF",
        data=st.session_state.generated_pdf,
        file_name=f"Questions_{topic_input.replace(' ', '_')}_{blooms_level[:2]}.pdf",
        mime="application/pdf",
    )

st.divider()
st.subheader("👨‍🏫 AI Examiner (Grading)")
st.info("Upload a photo of your handwritten answer, and EduRAG will grade it!")

# Input Form
with st.form("grading_form"):
    q_text = st.text_input(
        "1. Copy the Question here:", placeholder="e.g. Explain HDFS Architecture"
    )
    q_marks = st.number_input("2. Max Marks:", min_value=1, max_value=20, value=5)

    uploaded_answer = st.file_uploader(
        "3. Upload Handwritten Answer (Image)", type=["jpg", "jpeg", "png"]
    )

    submitted = st.form_submit_button("Grade My Answer")

if submitted:
    if not q_text or not uploaded_answer:
        st.warning("Please provide the question and upload an image.")
    else:
        with st.spinner("👀 Reading your handwriting and checking syllabus..."):
            # 1. Retrieve Context for this specific question
            # (We need to know what the syllabus says about this topic!)
            results, _ = similarity_search_from_db(q_text)

            if not results:
                context_text = "No specific context found. Grade based on general academic knowledge."
            else:
                context_text = "\n".join([doc.page_content for doc in results])

            # 2. Call the Grader
            result = grade_answer_image(q_text, context_text, uploaded_answer, q_marks)

            # 3. Display Results
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                st.balloons()

                # Layout for results
                col_grade, col_details = st.columns([1, 2])

                with col_grade:
                    st.metric(
                        label="Marks Awarded", value=result.get("marks_awarded", "N/A")
                    )
                    st.image(uploaded_answer, caption="Your Answer", width="content")

                with col_details:
                    st.subheader("📝 Feedback")
                    st.write(f"**Reasoning:** {result.get('reasoning')}")
                    st.info(f"**Improvement Tips:** {result.get('improvement_tips')}")

                    with st.expander("What the AI read (Transcription)"):
                        st.text(result.get("handwriting_transcription"))
