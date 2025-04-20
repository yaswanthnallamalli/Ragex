import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Example texts
texts = [
    "Company A had 5 incidents in March.",
    "Company B had 3 incidents in April."
]

# Load the real model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Generate real embeddings
embeddings = model.encode(texts, convert_to_numpy=True).astype(np.float32)

# Ensure directory exists
os.makedirs("vector_store/faiss_index", exist_ok=True)

# Save the texts
with open("vector_store/faiss_index/texts.pkl", "wb") as f:
    pickle.dump(texts, f)

# Create and save FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "vector_store/faiss_index/index.faiss")

print("✅ FAISS index and texts.pkl saved with real SentenceTransformer embeddings!")
