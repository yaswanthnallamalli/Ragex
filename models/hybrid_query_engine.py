import os
import sys
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import HUGGINGFACE_TOKEN, MISTRAL_LOCAL_PATH
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from vector_store.sql_executor import execute_sql_query

model_pipeline = None

def load_mistral_pipeline():
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
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    schema_info = cursor.fetchall()
    conn.close()

    # Format schema as list of columns with types
    schema_str = "\n".join([f"- {col[1]}: {col[2]}" for col in schema_info])
    return schema_str

def generate_sql_from_prompt(prompt: str, pipe, schema: str) -> str:
    formatted_prompt = f"""
You are a helpful assistant that converts natural language to SQL.
I have a table named "excel_data" with the following columns:
{schema}

Respond with only the SQL query.

### Input: {prompt}
### SQL:"""

    out = pipe(formatted_prompt, max_new_tokens=128, do_sample=False)[0]['generated_text']
    
    sql_raw = out.split("### SQL:")[-1].strip()
    sql_clean = sql_raw.replace("```sql", "").replace("```", "").strip()
    return sql_clean

def hybrid_query(prompt: str, db_path: str, table_name: str = "excel_data"):
    pipe = load_mistral_pipeline()

    # Get schema from the actual table
    schema = extract_table_schema(db_path, table_name)

    # Generate SQL based on natural language + dynamic schema
    sql_query = generate_sql_from_prompt(prompt, pipe, schema)
    
    print("🔹 Generated SQL:", sql_query)

    result = execute_sql_query(sql_query, db_path)
    return result
