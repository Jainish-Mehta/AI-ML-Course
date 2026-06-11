import sqlite3
from pathlib import Path

current_dir = Path(__file__).resolve().parent
db_path = current_dir / "user.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Injecting mock data...")
seed_data = [
    ('Alice', 'Smith', 'alice@example.com', 'admin', 12000.50),
    ('Bob', 'Jones', 'bob@example.com', 'customer', 450.00),
    ('Charlie', 'Brown', 'charlie@example.com', 'customer', 120.00),
    ('Diana', 'Prince', 'diana@example.com', 'engineer', 8500.00),
    ('Evan', 'Wright', 'evan@example.com', 'engineer', 9200.00),
    ('Fiona', 'Gallagher', 'fiona@example.com', 'customer', 50.00)
]

cursor.executemany("INSERT OR IGNORE INTO users (first_name, last_name, email, role, account_balance) VALUES (?, ?, ?, ?, ?)", seed_data)
conn.commit()   

print("\nMock data injected successfully.")
print("\nTotals and Averages ")
cursor.execute("SELECT SUM(account_balance), AVG(account_balance) FROM users")
totals = cursor.fetchone()
print(f'\nTotal Company Value: ${totals[0]:,.2f}')
print(f'Average user Balance: ${totals[1]:,.2f}')

print("\n<---Using GroupBy--->")
group_query = """
    SELECT role, AVG(account_balance), COUNT(user_id) 
    FROM users 
    GROUP BY role
    ORDER BY AVG(account_balance) DESC; -- Sorts from highest to lowest
"""
cursor.execute(group_query)
for row in cursor.fetchall():
    role = row[0].upper()
    avg_bal = row[1]
    headcount = row[2]
    print(f"Role: {role} | Headcount: {headcount} | Avg Balance: ${avg_bal:,.2f}")
    
print("\nTOP 2 Richest Customers")

top_customer_query ="""
    SELECT first_name,last_name,account_balance
    FROM users
    WHERE role = 'customer'
    ORDER BY account_balance DESC
    LIMIT 2
"""

cursor.execute(top_customer_query)
for rank,user in enumerate(cursor.fetchall(),1):
    print(f"#{rank} - {user[0]} {user[1]}: ${user[2]:,.2f}")
    
top_admin_query ="""
    SELECT first_name,last_name,account_balance
    FROM users
    WHERE role = 'admin'
    ORDER BY account_balance DESC
    LIMIT 2 
"""
cursor.execute(top_admin_query)
print("\nTOP 2 Richest Admins")
for rank,user in enumerate(cursor.fetchall(),1):
    print(f"#{rank} - {user[0]} {user[1]}: ${user[2]:,.2f}")
    
top_richest_query ="""
    SELECT first_name,last_name,account_balance
    FROM users
    ORDER BY account_balance DESC
    LIMIT 1
"""
cursor.execute(top_richest_query)
print("\nTOP 1 Richest Users")
for rank,user in enumerate(cursor.fetchall(),1):
    print(f"#{rank} - {user[0]} {user[1]}: ${user[2]:,.2f}")

conn.close()