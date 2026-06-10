import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
db_path = root / "db" / "fraud_detection" / "e-commerce.db"
sql_file_path = root / "sql"/ "fraud_detection"/ "products.sql" # customers.sql, products.sql, transactions.sql

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(sql_file_path, 'r') as file:
    query = file.read()
    
try: 
    cursor.executescript(query)
    conn.commit()
    print(f"Executed SQL script from {sql_file_path.name} successfully.")
except sqlite3.Error as e:
    print(f"An error occurred while executing the SQL script: {e}")
finally:
    conn.close()