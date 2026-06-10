import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
db_path = root /"db" / "crypto" / "crypto.db"
sql_file_path = root / "sql" / "crypto" / "crypto_price_history_table.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(sql_file_path, 'r') as file:
    sql_script = file.read()

try:
    cursor.executescript(sql_script)
    conn.commit()
    print("Crypto price history table created successfully.")
except sqlite3.Error as e:
    print(f"Error creating table: {e}")
finally:
    conn.close()