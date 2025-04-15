# ragex/test_sql_run.py

from vector_store.sql_executor import execute_sql_query

sql = "SELECT dv_company, COUNT(*) FROM excel_data GROUP BY dv_company"
results = execute_sql_query(sql, "vector_store/excel_db.sqlite")

for row in results:
    print(row)
