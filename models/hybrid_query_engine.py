import os
import sys
import sqlite3
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import HUGGINGFACE_TOKEN, MISTRAL_LOCAL_PATH
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from vector_store.sql_executor import execute_sql_query
from models.utils.column_matcher import match_columns_in_sql

model_pipeline = None

def load_mistral_pipeline():
    """
    Load the Mistral model pipeline for text generation.
    """
    global model_pipeline
    if model_pipeline is None:
        tokenizer = AutoTokenizer.from_pretrained(
            MISTRAL_LOCAL_PATH,
            token=HUGGINGFACE_TOKEN,
            cache_dir=MISTRAL_LOCAL_PATH
        )
        model = AutoModelForCausalLM.from_pretrained(
            MISTRAL_LOCAL_PATH,
            device_map="auto",
            load_in_4bit=True,
            trust_remote_code=True,
            token=HUGGINGFACE_TOKEN,
            cache_dir=MISTRAL_LOCAL_PATH
        )
        model_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return model_pipeline

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

    # Format schema as list of columns with types
    schema_str = "\n".join([f"- {col[1]}: {col[2]}" for col in schema_info])
    print("🔍 Table Schema for model:", schema_str)
    return schema_str

def generate_sql_from_prompt(prompt: str, pipe, schema: str) -> str:
    """
    Generate SQL query based on the input natural language prompt and table schema.
    """
    formatted_prompt = f"""
You are a helpful assistant that converts natural language into SQL queries.

You are allowed to use only one table: "excel_data".

Here is the table schema (column names and their types):
{schema}

⚠️ IMPORTANT INSTRUCTIONS:
- Use ONLY the column names from the schema above. Column names are case-sensitive.
- Do NOT guess or invent new column names.
- If the input mentions application-related categories (like 'Payments', 'Insurance', etc.), use the column 'application_category'.
- Your output must be a syntactically correct SQL query compatible with SQLite.
- Return only the SQL query — no extra explanation, markdown, or formatting.

### Input: {prompt}
### SQL:
"""

    output = pipe(formatted_prompt, max_new_tokens=128, do_sample=False)[0]["generated_text"]
    sql_raw = output.split("### SQL:")[-1].strip()
    sql_clean = sql_raw.replace("```sql", "").replace("```", "").strip() if sql_raw else ""

    # Match columns correctly to schema
    sql_final = match_columns_in_sql(sql_clean, schema)
    return sql_final


def hybrid_query(prompt: str, db_path: str, table_name: str = "excel_data"):
    """
    Perform a hybrid query by generating SQL from a natural language prompt and executing it.
    """
    pipe = load_mistral_pipeline()
    schema = extract_table_schema(db_path, table_name)
    sql_query = generate_sql_from_prompt(prompt, pipe, schema)

    print("🔹 Generated SQL:", sql_query)

    result = execute_sql_query(sql_query, db_path)
    
    if not result:
        print("⚠️ No results found for the query.")
        return None
    
    return result
