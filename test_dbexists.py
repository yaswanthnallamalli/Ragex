import lancedb

# Connect to the database
db = lancedb.connect("vector_store/lancedb")

# Print available tables
print(db.list_tables())  # This will show all tables in the database
