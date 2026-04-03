from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model():
    return HuggingFaceEmbeddings(model="google/embeddinggemma-300m")
    # return HuggingFaceEmbeddings(model="Qwen/Qwen3-Embedding-0.6B")
