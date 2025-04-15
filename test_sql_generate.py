from models.sql_query_generator import generate_sql_prompt, generate_sql_from_mistral
import pandas as pd

df = pd.read_csv("data/incident_data.csv", encoding="latin1")
query = "How many incidents in Hyderabad in 2023?"

prompt = generate_sql_prompt(query, df)
sql = generate_sql_from_mistral(prompt, "models/huggingface/hub")  # your Mistral cache path
print(sql)
