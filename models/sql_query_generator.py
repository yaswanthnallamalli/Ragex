# rag/models/sql_query_generator.py

import pandas as pd
import logging
from transformers import pipeline
from models.load_model import load_mistral_model

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def map_dtype(dtype) -> str:
    """Map pandas dtypes to general SQL-friendly types."""
    dtype = str(dtype)
    if 'int' in dtype:
        return 'integer'
    elif 'float' in dtype:
        return 'float'
    elif 'bool' in dtype:
        return 'boolean'
    elif 'datetime' in dtype:
        return 'timestamp'
    else:
        return 'text'


def generate_sql_prompt(user_question: str, df: pd.DataFrame, table_name: str = "excel_data") -> str:
    """
    Generate a prompt including table schema and few-shot examples.
    """
    # Prepare schema
    schema_lines = [f"{col}: {map_dtype(dtype)}" for col, dtype in df.dtypes.items()]
    schema_str = "\n".join(schema_lines)

    try:
        # Load few-shot examples from file in same folder
        with open("/mnt/f/sem-8/rag/models/few_shot_examples.txt", "r") as f:
            few_shot_examples = f.read().strip()
    except FileNotFoundError:
        logger.error("❌ few_shot_examples.txt file not found.")
        few_shot_examples = ""

    # Replace default placeholder table name with actual one
    few_shot_examples = few_shot_examples.replace("excel_data", table_name)

    # Final Prompt
    prompt = f"""
You are a helpful assistant that converts natural language questions to SQL queries.

Table: {table_name}
Schema:
{schema_str}

{few_shot_examples}

### Input: {user_question}
### SQL:
""".strip()

    return prompt


def generate_sql_from_mistral(prompt: str, model_path: str = None) -> str:
    """
    Uses Mistral model to generate SQL from the prompt.
    """
    tokenizer, model = load_mistral_model(model_path) if model_path else load_mistral_model()
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

    logger.info("🚀 Generating SQL from prompt...")
    output = generator(
        prompt,
        max_new_tokens=100,
        do_sample=False,
        temperature=0.0,
        pad_token_id=tokenizer.eos_token_id,
    )[0]["generated_text"]

    sql_start = output.rfind("### SQL:")
    if sql_start != -1:
        sql_chunk = output[sql_start + len("### SQL:"):].strip()
        sql_query = sql_chunk.split("###")[0].strip()
        logger.info(f"✅ Generated SQL: {sql_query}")
    else:
        logger.error("❌ Could not extract SQL from model output.")
        sql_query = ""

    return sql_query


# Optional: Fine-tuning support (skeleton)
def fine_tune_sql_model(training_data_path: str, model_save_path: str):
    """
    This function is a placeholder if you want to fine-tune the model on your SQL examples.
    You'd use Hugging Face's Trainer API with DPO/SFT etc.
    """
    raise NotImplementedError("This function is a placeholder for future fine-tuning.")
