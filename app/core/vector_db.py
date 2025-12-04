from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

qdrant = QdrantClient(
    url="https://YOUR-CLUSTER-URL.qdrant.cloud",
    api_key="YOUR_API_KEY"
)

collection_name = "edurag_syllabus"

# Create collection (run once)
def init_collection():
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

model = SentenceTransformer("all-MiniLM-L6-v2")

def store_chunks(chunks):
    points = []

    for c in chunks:
        embedding = model.encode(c["text"]).tolist()
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload=c
        )
        points.append(point)

    qdrant.upsert(collection_name=collection_name, points=points)
