# models/sql_query_generator.py

import logging
import sqlite3
from pathlib import Path

from models.utils.column_matcher import match_columns_in_sql
from models.load_model import load_mistral_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "vector_store/excel_db.sqlite"
TABLE_NAME = "excel_data"
FEW_SHOT_FILE = "models/few_shot_examples.txt"

def get_db_schema():
    """Retrieve schema from the SQLite DB."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({TABLE_NAME});")
    columns = cursor.fetchall()
    conn.close()
    schema_lines = [f"{col[1]}: {col[2]}" for col in columns]
    schema = "\n".join(schema_lines)
    return schema

def load_few_shot_examples():
    """Load few-shot examples from text file."""
    path = Path(FEW_SHOT_FILE)
    if not path.exists():
        logger.warning(f"{FEW_SHOT_FILE} not found!")
        return ""
    return path.read_text()

def generate_sql_prompt(user_query: str) -> str:
    logger.info("📜 Generating SQL prompt...")
    schema = get_db_schema()
    few_shots = load_few_shot_examples()

    prompt = f"""You are a helpful assistant that converts natural language questions to SQL queries.

Table: {TABLE_NAME}
Schema:
{schema}

{few_shots}
### Input: {user_query}
### SQL:"""
    return prompt

def generate_sql_from_mistral(prompt: str) -> str:
    logger.info("🚀 Generating SQL from prompt...")
    model = load_mistral_pipeline()
    raw_sql = model(prompt, max_new_tokens=256)[0]["generated_text"]
    
    # Postprocess: strip prompt prefix from generated output
    generated_sql = raw_sql.split("### SQL:")[-1].strip().split("\n")[0]

    # Schema match correction
    schema = get_db_schema()
    fixed_sql = match_columns_in_sql(generated_sql, schema)

    logger.info(f"✅ Generated SQL: {fixed_sql}")
    return fixed_sql
