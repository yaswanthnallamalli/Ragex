# test_sql_generate.py

from models.sql_query_generator import generate_sql_prompt, generate_sql_from_mistral

# Natural language query
query = "Show all high priority incidents from the year 2023."

# Generate prompt using schema and few-shot examples
prompt = generate_sql_prompt(query)

# Print the generated prompt (optional, for debugging)
print("📜 Generated Prompt:")
print(prompt)

# Generate SQL using Mistral
sql = generate_sql_from_mistral(prompt)

# Print the generated SQL
print("\n✅ Generated SQL:")
print(sql)
