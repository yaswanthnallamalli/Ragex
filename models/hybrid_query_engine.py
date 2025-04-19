# models/hybrid_query_engine.py
import os
import sys
import sqlite3
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vector_store.sql_executor import execute_sql_query
from models.utils.column_matcher import match_columns_in_sql
from models.load_model import load_mistral_pipeline

def extract_table_schema(db_path: str, table_name: str) -> str:
    """
    Extract the schema of the given SQLite table.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    schema_info = cursor.fetchall()
    conn.close()

    if not schema_info:
        raise ValueError(f"Could not retrieve schema for table {table_name}")

    schema_str = "\n".join([f"- {col[1]}: {col[2]}" for col in schema_info])
    print("🔍 Table Schema:", schema_str)
    return schema_str

def generate_sql_from_prompt(prompt: str, pipe, schema: str) -> str:
    """
    Generate SQL query based on the prompt and table schema.
    """
    formatted_prompt = f"""
You are a helpful assistant that converts natural language into SQL queries.

You are allowed to use only one table: "excel_data".

Here is the table schema:
{schema}

⚠️ IMPORTANT:
- Use only the listed columns (case-sensitive).
- Do not invent columns.
- Output only valid SQLite-compatible SQL.

### Input: {prompt}
### SQL:
"""

    output = pipe(formatted_prompt, max_new_tokens=128, do_sample=False)[0]["generated_text"]
    sql_raw = output.split("### SQL:")[-1].strip()
    sql_clean = sql_raw.replace("```sql", "").replace("```", "").strip() if sql_raw else ""
    return match_columns_in_sql(sql_clean, schema)

def hybrid_query(prompt: str, db_path: str, table_name: str = "excel_data"):
    """
    Generates SQL from prompt, executes it, and returns result.
    """
    pipe = load_mistral_pipeline()
    schema = extract_table_schema(db_path, table_name)
    sql_query = generate_sql_from_prompt(prompt, pipe, schema)

    print("🔹 Generated SQL:", sql_query)

    result = execute_sql_query(sql_query, db_path)
    if not result:
        print("⚠️ No results found.")
        return None

    return result
