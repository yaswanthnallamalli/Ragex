# rag/models/sql_query_generator.py

import pandas as pd
import logging
from transformers import pipeline
from models.load_model import load_mistral_model

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sql_prompt(user_question: str, df: pd.DataFrame, table_name: str = "excel_data") -> str:
    """
    Generates a SQL-style prompt from user question and table schema for LLM input.

    Args:
        user_question (str): User's natural language query.
        df (pd.DataFrame): The data schema used for SQL context.
        table_name (str): Name of the SQL table (default: excel_data).

    Returns:
        str: Formatted prompt with schema and few-shot examples.
    """
    schema_lines = [f"- {col} ({str(dtype)})" for col, dtype in df.dtypes.items()]
    schema_str = "\n".join(schema_lines)

    prompt = f"""
You are a helpful assistant that converts natural language to SQL queries.

Table: {table_name}
Columns:
{schema_str}

### Input: Get total revenue in 2023
### SQL: SELECT SUM(revenue) FROM {table_name} WHERE year = 2023;

### Input: List all cities with more than 100 incidents
### SQL: SELECT city FROM {table_name} WHERE incidents > 100;

### Input: {user_question}
### SQL:
"""
    return prompt.strip()


def generate_sql_from_mistral(prompt: str) -> str:
    """
    Generates SQL query from natural language prompt using Mistral LLM.

    Args:
        prompt (str): The input prompt including schema and user query.

    Returns:
        str: SQL query string.
    """
    tokenizer, model = load_mistral_model()

    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    logger.info("🚀 Generating SQL from prompt...")
    output = generator(prompt, max_new_tokens=150, do_sample=True, top_p=0.9)[0]["generated_text"]

    sql_start = output.rfind("### SQL:")
    if sql_start != -1:
        sql_query = output[sql_start + len("### SQL:"):].strip()
        logger.info(f"✅ Generated SQL: {sql_query}")
    else:
        logger.error("❌ Could not extract SQL from model output.")
        sql_query = ""

    return sql_query
