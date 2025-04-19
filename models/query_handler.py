import os
import lancedb
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

from models.sql_query_generator import generate_sql_from_mistral
from models.hybrid_query_engine import hybrid_query

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def query_handler(user_query: str, db_path: str, table_name: str):
    """
    Main handler for processing user queries.
    Routes between SQL and general embedding-based search.
    """
    if is_sql_query(user_query):
        sql_query = generate_sql_from_mistral(user_query)
        results = execute_sql_query(sql_query, db_path)
        return results
    else:
        return process_general_query(user_query, db_path, table_name)

def is_sql_query(query: str) -> bool:
    """
    Heuristic to detect if a user query is SQL-like.
    """
    sql_keywords = ["select", "from", "where", "group by", "order by"]
    return any(keyword in query.lower() for keyword in sql_keywords)

def process_general_query(user_query: str, db_path: str, table_name: str):
    """
    Process general (non-SQL) queries using vector search on LanceDB.
    """
    # Connect to LanceDB
    db = lancedb.connect(os.path.abspath(db_path))
    table = db.open_table(table_name)

    # Embed the user query (convert to float32 to match LanceDB schema)
    query_embedding = embedding_model.encode(user_query, convert_to_numpy=True).astype(np.float32).tolist()

    # Search top-k similar entries using vector index
    results = (
        table.search(query_embedding, vector_column_name="embedding")
        .limit(5)
        .to_pandas()
    )

    relevant_data = results["text"].tolist()
    return generate_answer_from_model(relevant_data, user_query)

def generate_answer_from_model(relevant_data, user_query):
    """
    Uses Mistral model to generate an answer using RAG with the retrieved context.
    """
    return hybrid_query(user_query, db_path=os.path.abspath("vector_store/lancedb"), table_name="excel_embeddings")

def execute_sql_query(sql_query: str, db_path: str):
    """
    Executes SQL query on a SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchall()
    conn.close()
    return result
