# rag/models/embedding_generator.py
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

def embed_excel_to_faiss(file_path="data/incident_data.csv", index_path="rag/vector_store/faiss_index"):
    # Read and preprocess
    df = pd.read_csv(file_path, encoding='latin1')
    df["text"] = df.astype(str).agg(" | ".join, axis=1)

    # Generate embeddings
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(df["text"].tolist(), convert_to_numpy=True)

    # Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Save index and text
    os.makedirs(index_path, exist_ok=True)
    faiss.write_index(index, os.path.join(index_path, "index.faiss"))
    with open(os.path.join(index_path, "texts.pkl"), "wb") as f:
        pickle.dump(df["text"].tolist(), f)

    print("✅ FAISS index created and saved.")

# Auto run if file exists
# if __name__ == "__main__":
#     file_path = "data/incident_data.csv"
#     if os.path.exists(file_path):
#         embed_excel_to_faiss(file_path)
#     else:
#         print(f"❌ File not found: {file_path}")
