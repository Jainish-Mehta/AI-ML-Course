import sqlite3
from pathlib import Path

current_dir = Path(__file__).resolve().parent
sql_file_path = current_dir / "Purchases.sql"
db_path = current_dir / "Database.db"

print("Connecting to Database...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(sql_file_path,'r') as file:
    sql_script = file.read()
try:
    cursor.executescript(sql_script)
    conn.commit()
    print("Database created successfully.")
except sqlite3.Error as e:
    print(f"Error: {e}")
finally:
    conn.close()