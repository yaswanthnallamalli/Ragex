from models.sql_query_generator import generate_sql_prompt, generate_sql_from_mistral
import pandas as pd

df = pd.read_csv("data/incident_data.csv", encoding="latin1")
query = "List all incidents in Hyderabad in 2023"

prompt = generate_sql_prompt(query, df)

# Use full path to Mistral snapshot
model_path = "models/huggingface/hub/models--mistralai--Mistral-7B-Instruct-v0.2/snapshots/3ad372fc79158a2148299e3318516c786aeded6c"

sql = generate_sql_from_mistral(prompt, model_path)
print(sql)
