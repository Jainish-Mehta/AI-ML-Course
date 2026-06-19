import sqlite3
import numpy as np
from pathlib import Path

# 🛑 PRO ROUTING: Point directly to the data/ folder
root = Path(__file__).resolve().parent.parent.parent
db_path = root / "db" / "advance_fraud_detection" / "ab_testing.db"

def initialize_and_seed_db():
    """Builds the database and seeds it with poisoned A/B test data."""
    # Ensure the data folder exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS transactions;")
        cursor.execute("""
            CREATE TABLE transactions (
                tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_group TEXT NOT NULL,
                purchase_amount REAL NOT NULL
            );
        """)
        
        # Generate Normal Data 
        np.random.seed(42) 
        group_a_normal = np.random.normal(loc=15000.0, scale=10.0, size=500)
        group_b_normal = np.random.normal(loc=15500.0, scale=10.0, size=500)
        
        # THE POISON: Inject 3 massive $15,000 fraud transactions into Group A
        group_a_poisoned = np.append(group_a_normal, [15000.0, 15500.0, 14900.0])
        
        a_data = [("A", float(val)) for val in group_a_poisoned]
        b_data = [("B", float(val)) for val in group_b_normal]
        all_data = a_data + b_data
        
        np.random.shuffle(all_data)
        cursor.executemany("INSERT INTO transactions (test_group, purchase_amount) VALUES (?, ?);", all_data)
        conn.commit()

def fetch_group_data(group_name):
    """Extracts raw data for a specific group from the DB."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_amount FROM transactions WHERE test_group = ?;", (group_name,))
        data = cursor.fetchall()
        
    return np.array([row[0] for row in data])