# ragex/vector_store/sql_executor.py

import sqlite3

def execute_sql_query(sql_query: str, db_path: str, table_name: str = "excel_data") -> list:
    """
    Execute the generated SQL query on the SQLite DB.
    """
    try:
        # Using 'with' statement for automatic resource management
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)

            # Ensure that cursor.description is not None before processing
            if cursor.description:
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
            else:
                print("❌ No columns in the result.")
                result = []

        print("✅ SQL executed successfully.")
        return result

    except sqlite3.Error as e:
        print("❌ SQLite Error:", e)
        return []
