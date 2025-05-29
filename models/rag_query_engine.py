# rag/models/rag_query_engine.py
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from models.load_model import load_mistral_pipeline

# Load everything
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
llm = load_mistral_pipeline()

# Load FAISS index and text data
index = faiss.read_index("vector_store/faiss_index/index.faiss")
with open("vector_store/faiss_index/texts.pkl", "rb") as f:
    documents = pickle.load(f)

def search_similar_rows(query, k=5):
    query_embedding = embedding_model.encode([query]).astype(np.float32)
    print(f"🔍 Query embedding shape: {query_embedding.shape}")         # <-- ADD THIS
    print(f"📦 FAISS index dimension: {index.d}")                      # <-- ADD THIS
    if query_embedding.shape[1] != index.d:
        raise ValueError(f"❌ Dimension mismatch! Query embedding is {query_embedding.shape[1]},"f"but FAISS index expects {index.d}")
    distances, indices = index.search(query_embedding, k)
    return [documents[i] for i in indices[0]]


def generate_rag_answer(query: str):
    context_chunks = search_similar_rows(query)
    context = "\n".join(context_chunks)
    
    prompt = f"""Answer the question based on the following context:\n\n{context}\n\nQuestion: {query}\nAnswer:"""
    
    response = llm(prompt, max_new_tokens=150)[0]["generated_text"]

    # Extract only the text after "Answer:"
    if "Answer:" in response:
        answer_text = response.split("Answer:")[-1].strip()
    else:
        answer_text = response.strip()

    # Limit to 150 words
    answer_words = answer_text.split()
    if len(answer_words) > 150:
        answer_text = " ".join(answer_words[:150]) + "..."
    print("🔎 Raw LLM output:\n", response)


    return answer_text

# Local testing loop
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (or type 'exit'): ")
        if user_query.lower() == "exit":
            break
        answer = generate_rag_answer(user_query)
        print("\n📘 Answer:", answer)
