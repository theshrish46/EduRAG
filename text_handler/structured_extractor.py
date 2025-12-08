from models.llm_model import get_llm_model

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import load_prompt


template = load_prompt("SYLLABUS_PROMPT.json")
model = get_llm_model()

def cleaned_text_extractor(syllabus_text):
    prompt = template.invoke({"syllabus_text": syllabus_text})
    result = model.invoke(prompt)
    print(result)
    return result.content
