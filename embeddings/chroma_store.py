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

# Use this raw collection object for fast lookups
collection = client.get_or_create_collection("syllabus_embeddings")

vector_store = Chroma(
    client=client,
    collection_name="syllabus_embeddings",
    embedding_function=embedding_model,
)


def check_file_exists(filename):
    """
    Fast check to see if we already have chunks from this file.
    """
    try:
        # We query the raw collection for any doc having this source
        existing = collection.get(
            where={"source": filename},
            limit=1,  # We only need to know if 1 chunk exists
        )
        return len(existing["ids"]) > 0
    except Exception as e:
        print(f"Error checking DB: {e}")
        return False


def create_chroma_from_docs(chunks, meta_data):
    # Ensure IDs are unique
    ids = [str(uuid4()) for _ in range(len(chunks))]
    vector_store.add_texts(texts=chunks, metadatas=meta_data, ids=ids)


def similarity_search_from_db(user_prompt):
    print(user_prompt)
    results = vector_store.similarity_search(
        user_prompt, k=3
    )  # Reduced k to 5 for cleaner results

    output_list = []
    for r in results:
        output_list.append({"page_content": r.page_content, "meta_data": r.metadata})

    return results, output_list
