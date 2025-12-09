import os, sys
import chromadb
from uuid import uuid4
from dotenv import load_dotenv
from langchain_chroma import Chroma

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.embedding_model import get_embedding_model

embedding_model = get_embedding_model()

load_dotenv()

client = chromadb.CloudClient(
    api_key=os.getenv("CHROMA_API_KEY"),
    tenant=os.getenv("CHROMA_TENANT"),
    database=os.getenv("CHROMA_DATABASE"),
)

collection = client.get_or_create_collection("syllabus_embeddings")


vector_store = Chroma(
    client=client,
    collection_name="syllabus_embeddings",
    embedding_function=embedding_model,
)


def create_chroma_from_docs(chunks, meta_data):
    ids = [str(uuid4()) for _ in range(len(chunks))]

    vector_store.add_texts(texts=chunks, metadatas=meta_data, ids=ids)


def similarity_search_from_db(user_prompt):
    print(user_prompt)

    results = vector_store.similarity_search(user_prompt, k=11)
    for r in results:
        json_output = {
            "id": r.id,
            "meta_data": r.metadata,
            "page_content": r.page_content,
        }
    return results, json_output
