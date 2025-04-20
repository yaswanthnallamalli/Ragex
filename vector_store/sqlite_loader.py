# rag/vector_store/sqlite_loader.py
import pandas as pd
import sqlite3
import os

def excel_to_sqlite(file_path: str, db_path: str, table_name: str = "excel_data"):
    # Auto-detect file type and load
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path,encoding="latin1")
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .csv or .xlsx")

    print(f"✅ {ext.upper()} loaded with shape:", df.shape)

    # Create directory if not exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Save to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"✅ Data saved to '{db_path}' in table '{table_name}'")