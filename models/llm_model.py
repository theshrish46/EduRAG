from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

import os

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

llm = HuggingFaceEndpoint(
    repo_id= "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    task= "text-generation",
    huggingfacehub_api_token=HF_TOKEN
)

def get_llm_model():
    return ChatHuggingFace(llm=llm)