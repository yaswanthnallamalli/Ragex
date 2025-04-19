from models.query_handler import query_handler  # Corrected import path

# Example user queries
user_sql_query = "What is the total revenue for 2023?"
user_general_query = "Which company had the highest number of incidents?"

# Path to your database (Ensure the path to your DB is correct)
db_path = "vector_store/lancedb"  # Corrected path to the directory where your LanceDB is stored

# Table name in your LanceDB/SQL
table_name = "excel_embeddings"  # Name of your table in LanceDB

# Process SQL-like query
print("🔍 Processing SQL-like query...")
sql_results = query_handler(user_sql_query, db_path, table_name)
print("✅ SQL Query Results:", sql_results)

# Process general query
print("🔍 Processing general query...")
general_results = query_handler(user_general_query, db_path, table_name)
print("✅ General Query Answer:", general_results)
