# rag/models/lance_embedding_gen.py

import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer
import lancedb

def embed_excel_to_lancedb(file_path="data/incident_data.csv", db_path="rag/vector_store/lancedb"):
    # Load and preprocess
    df = pd.read_csv(file_path, encoding='latin1')
    df["text"] = df.astype(str).agg(" | ".join, axis=1)

    # Generate embeddings
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    texts = df["text"].tolist()
    embeddings = model.encode(texts, convert_to_numpy=True)

    # Prepare LanceDB
    os.makedirs(db_path, exist_ok=True)
    db = lancedb.connect(db_path)

    # Remove old table if it exists
    if "rag_table" in db.table_names():
        db.drop_table("rag_table")

    # Combine text and embeddings into records
    records = [{"text": text, "embedding": embedding.tolist()} for text, embedding in zip(texts, embeddings)]

    # Create new table
    db.create_table("rag_table", data=records)

    print("✅ LanceDB embeddings stored successfully.")

# Run this to auto-process if needed
if __name__ == "__main__":
    embed_excel_to_lancedb()
