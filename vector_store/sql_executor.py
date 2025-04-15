# ragex/vector_store/sql_executor.py

import sqlite3

def execute_sql_query(sql_query: str, db_path: str, table_name: str = "excel_data") -> list:
    """
    Execute the generated SQL query on the SQLite DB.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        conn.close()

        print("✅ SQL executed successfully.")
        return [dict(zip(columns, row)) for row in rows]

    except sqlite3.Error as e:
        print("❌ SQLite Error:", e)
        return []
