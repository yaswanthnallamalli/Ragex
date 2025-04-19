import re
from difflib import get_close_matches

def extract_column_names_from_schema(schema_str: str):
    lines = schema_str.strip().split('\n')
    return [line.split(':')[0].strip().lstrip('-').strip() for line in lines]

def match_columns_in_sql(sql: str, schema_str: str) -> str:
    schema_columns = extract_column_names_from_schema(schema_str)
    schema_map = {col.lower(): col for col in schema_columns}
    print("🔍 Clean Schema Columns:", schema_map)

    words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", sql)

    for word in set(words):
        if word in schema_columns:
            continue
        word_lower = word.lower()
        match = get_close_matches(word_lower, schema_map.keys(), n=1, cutoff=0.8)
        if match:
            correct_col = schema_map[match[0]]
            sql = re.sub(rf'\b{word}\b', correct_col, sql)

    return sql
