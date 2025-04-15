# ragex/test_hybrid.py

from models.hybrid_query_engine import hybrid_query

def test_hybrid_query():
    prompt = "Which company has the highest number of incidents?"
    db_path = "vector_store/excel_db.sqlite"  # Path to the SQLite database

    print(f"🔍 Running hybrid query for prompt: \"{prompt}\"")
    result = hybrid_query(prompt, db_path)  # No need for excel_file_path here

    if result:
        print("✅ Query Results:")
        for row in result:
            print(row)
    else:
        print("⚠️ No results returned from the query.")

if __name__ == "__main__":
    test_hybrid_query()
