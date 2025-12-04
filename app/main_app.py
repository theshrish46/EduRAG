import streamlit as st
import os

from core.utils import extract_text     # MUST correctly handle pdf/docx/image
from core.clean_text import clean_syllabus_text
from core.structure_syllabus import (
    split_into_modules,
    extract_unit_title,
    build_chunk_json
)

# --------------------------------------------------------
# 0. INITIAL SETUP
# --------------------------------------------------------
save_directory = "../data/uploaded_files"
os.makedirs(save_directory, exist_ok=True)

st.title("EduRAG")
st.write("One place solution to all your exam prep")

user_input = st.chat_input(
    "Upload your syllabus or enter a topic",
    accept_file=True,
    file_type=["pdf", "doc", "docx", "png", "jpeg", "jpg"],
    key="input_key",
)

# Store user chat
if "user_messages" not in st.session_state:
    st.session_state.user_messages = []


# --------------------------------------------------------
# 1. HANDLE FILE UPLOAD
# --------------------------------------------------------
if user_input:

    for upload_file in user_input.files:

        file_name = upload_file.name
        save_path = os.path.join(save_directory, file_name)
        st.write(f"📄 Uploaded: **{file_name}**")

        # ---- Save file ----
        try:
            with open(save_path, "wb") as f:
                f.write(upload_file.getbuffer())
            st.success(f"Saved to: `{save_path}`")
        except Exception as e:
            st.error(f"Error saving file: {e}")
            continue

        # --------------------------------------------------------
        # 2. EXTRACT TEXT (PDF / DOCX / IMG)
        # --------------------------------------------------------
        st.write("🔍 Extracting text...")

        extracted_text = extract_text(save_path, upload_file.type)

        if not extracted_text or extracted_text.strip() == "":
            st.error("❌ Failed to extract text from this file (OCR/format issue).")
            continue

        if not extracted_text or extracted_text is None or extracted_text == []:
            st.error("❌ Could not extract text from this file. Try uploading a clearer PDF/image.")
            continue

        st.success("✅ Text extracted successfully!")


        # --------------------------------------------------------
        # 3. CLEAN + STRUCTURE
        # --------------------------------------------------------
        cleaned_text, structured = clean_syllabus_text(extracted_text)

        st.subheader("📚 Extracted Structure")
        st.json(structured)


        # --------------------------------------------------------
        # 4. SPLIT INTO MODULES & CHUNK
        # --------------------------------------------------------
        st.write("🧩 Splitting into modules...")
        st.write(cleaned_text)

        modules = split_into_modules(cleaned_text)

        if not modules:
            st.error("❌ Could not detect modules in the text.")
            continue

        st.success(f"Detected **{len(modules)}** modules.")


        # --------------------------------------------------------
        # 5. BUILD JSON CHUNKS FOR VECTOR DB
        # --------------------------------------------------------
        st.write("⚙️ Building chunks...")

        all_chunks = []

        for module_name, module_text in modules:

            unit_title = extract_unit_title(module_name)

            # break into meaningful paragraphs
            paragraphs = [
                p.strip() for p in module_text.split("\n")
                if len(p.strip()) > 25
            ]

            for para in paragraphs:
                chunk_json = build_chunk_json(
                    module_name=module_name,
                    unit_title=unit_title,
                    text_block=para
                )
                all_chunks.append(chunk_json)

        st.success(f"Generated **{len(all_chunks)}** chunks for Vector DB.")
        st.json(all_chunks[:5])  # preview first 5


        # --------------------------------------------------------
        # (OPTIONAL)
        # 6. STORE IN VECTOR DB
        # --------------------------------------------------------
        # store_chunks(all_chunks)
        # st.success("🟢 Stored in Vector DB successfully!")