from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI

import os

load_dotenv()
# HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
)


def get_llm_model():
    return ChatHuggingFace(llm=llm)


def get_genai_model():
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
