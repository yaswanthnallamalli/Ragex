import os
import pandas as pd
import uuid
import numpy as np
import lancedb
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

# Constants
LANCEDB_PATH = "vector_store/lancedb"
TABLE_NAME = "excel_embeddings"
DATA_DIR = "data"
EMBEDDING_DIM = 384  # MiniLM output dimension

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def detect_encoding(file_path: str) -> str:
    import chardet
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result['encoding']

def load_data(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    elif ext == ".csv":
        encoding = detect_encoding(file_path)
        return pd.read_csv(file_path, encoding=encoding)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")

def generate_text_chunks(df: pd.DataFrame):
    return df.astype(str).apply(lambda row: " | ".join(row.values), axis=1).tolist()

# Pydantic model for embeddings
class EmbeddingSchema(BaseModel):
    id: str
    text: str
    embedding: list[float]  # Store embeddings as a list of floats

def embed_and_store(file_path: str):
    df = load_data(file_path)
    texts = generate_text_chunks(df)
    embeddings = embedding_model.encode(texts, convert_to_numpy=True).astype(np.float32)

    data_to_store = [
        EmbeddingSchema(id=str(uuid.uuid4()), text=text, embedding=embedding.tolist()).dict()  # Convert to dict
        for text, embedding in zip(texts, embeddings)
    ]

    os.makedirs(LANCEDB_PATH, exist_ok=True)
    db = lancedb.connect(LANCEDB_PATH)

    if TABLE_NAME in db.table_names():
        table = db.open_table(TABLE_NAME)
        table.add(data_to_store)
    else:
        table = db.create_table(TABLE_NAME, data_to_store)

    print(f"✅ Stored {len(data_to_store)} rows in LanceDB table '{TABLE_NAME}'.")

if __name__ == "__main__":
    file_path = os.path.join(DATA_DIR, "incident_data.csv")
    embed_and_store(file_path)
