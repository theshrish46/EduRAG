from models.llm_model import get_llm_model, get_genai_model

import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import JsonOutputParser


parser = JsonOutputParser()

template = load_prompt("SYLLABUS_PROMPT.json")
model = get_genai_model()

chain = template | model | parser


def cleaned_text_extractor(syllabus_text):
    # prompt = template.invoke({"syllabus_text": syllabus_text})
    chain = template | model | parser
    result = chain.invoke({"syllabus_text": syllabus_text})
    return result
