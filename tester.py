from vector_store.sqlite_loader import excel_to_sqlite

excel_to_sqlite(
    file_path="data/incident_data.csv",
    db_path="vector_store/excel_db.sqlite",
    table_name="excel_data"
)
