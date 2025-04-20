import lancedb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
db = lancedb.connect("ragex/vector_store/lancedb")
table = db.open_table("rag_table")

def search_rag_context(query, k=3):
    query_embedding = model.encode([query])[0]
    results = table.search(query_embedding).limit(k).to_pandas()
    return results["text"].tolist()
