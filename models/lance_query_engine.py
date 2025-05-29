# rag/models/lance_query_engine.py

import lancedb
import numpy as np
from sentence_transformers import SentenceTransformer
from models.load_model import load_mistral_pipeline

# Load the embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load the LLM
llm = load_mistral_pipeline()

# Connect to LanceDB and open the table
db = lancedb.connect("vector_store/lancedb")
table = db.open_table("rag_table")  # Table should already exist with 'text' and 'embedding' columns

def search_similar_rows(query, k=5):
    # Generate the query embedding
    query_embedding = embedding_model.encode([query])[0].tolist()
    print(f"🔍 Query embedding length: {len(query_embedding)}")

    # Perform similarity search using LanceDB
    results = table.search(query_embedding).limit(k).to_pandas()
    return results["text"].tolist()

def generate_rag_answer(query: str):
    context_chunks = search_similar_rows(query)
    context = "\n".join(context_chunks)
    prompt = f"""Answer the question based on the following context:\n\n{context}\n\nQuestion: {query}\nAnswer:"""
    return llm(prompt)

# Optional testing loop
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (or type 'exit'): ")
        if user_query.lower() == "exit":
            break
        answer = generate_rag_answer(user_query)
        print("\n📘 Answer:", answer)
