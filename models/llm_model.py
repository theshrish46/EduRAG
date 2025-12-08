from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv


load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id= "Qwen/Qwen3-Coder-30B-A3B-Instruct",
    task= "text-generation"
)

def get_llm_model():
    return ChatHuggingFace(llm=llm)