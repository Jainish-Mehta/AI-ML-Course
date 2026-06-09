import sqlite3
from pathlib import Path

current_path = Path(__file__).resolve().parent

db_path = current_path / "Database.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()  

inner_join_query = """
    SELECT u.first_name, u.last_name, pr.product_name, pr.price, p.purchase_date
    FROM users u
    INNER JOIN purchases p ON u.user_id = p.user_id
    INNER JOIN products pr ON p.product_id = pr.product_id
"""
cursor.execute(inner_join_query)
print("\n<---INNER JOIN Example--->")
for row in cursor.fetchall():
    print(f"{row[0]} {row[1]} bought {row[2]} for ${row[3]:,.2f}")
    
print("\n<---LEFT JOIN Example--->")
left_join_query = """
    SELECT u.first_name, u.last_name, pr.product_name, pr.price, p.purchase_date
    FROM users u
    LEFT JOIN purchases p ON u.user_id = p.user_id
    LEFT JOIN products pr ON p.product_id = pr.product_id
"""
    
cursor.execute(left_join_query)
for row in cursor.fetchall():
    product = row[2] if row[2] else "Nothing"
    price = f"${row[3]:,.2f}" if row[3] else "$0.00"
    if row[2] is None:
        print(f"{row[0]} {row[1]} has not made any purchases.")
    else:
        print(f"{row[0]} {row[1]} bought {product} for {price}")
        
print("\n<---RIGHT JOIN Example--->")
right_join_query ="""
    SELECT pr.product_name, COUNT(pr.product_name), AVG(pr.price), SUM(pr.price)
    FROM products pr
    RIGHT JOIN purchases p ON p.product_id = pr.product_id
    GROUP BY pr.product_name
"""

print("Products that have been purchased:")
cursor.execute(right_join_query)
sum_price = 0
for row in cursor.fetchall():
    sum_price += row[3] if row[3] else 0
    print(f"{row[1]} {row[0]} for ${row[2]:,.2f}")

print(f"\nTotal PAID for all products: ${sum_price:,.2f}")
    
full_join_query = """
    SELECT u.first_name, u.last_name, pr.product_name, pr.price, p.purchase_date
    FROM users u
    FULL JOIN purchases p ON u.user_id = p.user_id
    FULL JOIN products pr ON p.product_id = pr.product_id
"""
cursor.execute(full_join_query)
print("\n<---FULL JOIN Example--->")
for row in cursor.fetchall():
    new_row = list(row)
    for i in range(len(new_row)):
        if new_row[i] is None:
            
            new_row[i] = 0
    print(f"{new_row[0]} {new_row[1]} bought {new_row[2]} for ${new_row[3]:,.2f} on {new_row[4]}")
conn.close()
