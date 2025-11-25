import streamlit as st
import os
from core.utils import extract_text


save_directory = "../data/uploaded_files"
os.makedirs(save_directory, exist_ok=True)

st.title("EduRAG", width="stretch")
st.write("One place solution to all your exam prep")

user_input = st.chat_input(
    "Enter your desired topic",
    accept_file=True,
    file_type=["pdf", "docs", "docx", "png", "jpeg", "jpg"],
    key="first_key",
)


if "user_message" not in st.session_state:
    st.session_state.user_message = []

if user_input:
    st.session_state.user_message.append(user_input.text)
    st.write("User input", user_input.text)
    st.write("Users Messages", st.session_state.user_message)
    for i in range(len(st.session_state.user_message)):
        st.write(f"{i} -- {st.session_state.user_message[i]}")

    for upload_file in user_input.files:
        file_name = upload_file.name
        save_path = os.path.join(save_directory, file_name)
        print(f"Save ath {save_path}")

        # Save uploaded files

        with open(save_path, "wb") as f:
            f.write(upload_file.getbuffer())
        st.success(f"File saved successfully {file_name} at {save_path}")

        # Extract Text
        extracted_text = extract_text(save_path, upload_file.type)

        if extracted_text:
            st.success(f"Extracted text successfully")
            st.write(extracted_text)
        else:
            st.error(f"Failed to extract text, {extracted_text}")
