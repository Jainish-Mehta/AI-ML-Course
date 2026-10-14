import sqlite3
import random
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent
db_path = root / "db" / "fraud_detection" / "e-commerce.db"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    
    print("Injecting Customers and Products...")
    customers = [
        ('Alice Normal', 'alice@email.com'), 
        ('Bob Standard', 'bob@email.com'), 
        ('Charlie Inactive', 'charlie@email.com'), 
        ('Scammer Sam', 'sam@fraud.com')           
    ]
    products = [('Laptop', 1200.00, 'Electronics'), ('Mouse', 25.00, 'Accessories'), ('Headphones', 150.00, 'Accessories')]
    
    cursor.executemany("INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)", customers)
    cursor.executemany("INSERT OR IGNORE INTO products (product_name, price, category) VALUES (?, ?, ?)", products)
    
    print("Simulating organic user traffic...")
    for _ in range(30):
        c_id = random.choice([1, 2])
        p_id = random.choice([1, 2, 3])
        cursor.execute("INSERT INTO transactions (customer_id, product_id) VALUES (?, ?)", (c_id, p_id))

    print("Simulating malicious transaction spike...")
    for _ in range(50):
        p_id = random.choice([1, 2, 3])
        cursor.execute("INSERT INTO transactions (customer_id, product_id) VALUES (?, ?)", (4, p_id))

    conn.commit()


    print("\n" + "="*50)
    print(" DAILY SECURITY & SALES REPORT ")
    print("="*50)

    print("\n[TOP SELLING PRODUCTS]")
    revenue_query = """
        SELECT p.product_name, COUNT(t.transaction_id) as units_sold, SUM(p.price) as gross_revenue
        FROM products p
        INNER JOIN transactions t ON p.product_id = t.product_id
        GROUP BY p.product_name
        ORDER BY gross_revenue DESC;
    """
    for row in cursor.execute(revenue_query):
        print(f"- {row[0]}: {row[1]} units sold (Revenue: ${row[2]:,.2f})")


    print("\n[CHURN WARNING: INACTIVE USERS]")
    churn_query = """
        SELECT c.name, c.email
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        WHERE t.transaction_id IS NULL;
    """
    for row in cursor.execute(churn_query):
        print(f"- {row[0]} ({row[1]}) registered but bought nothing. Send retention email.")


    print("\n[FRAUD ALERT: ABNORMAL SPENDING]")
    
    fraud_query = """
        SELECT c.name, COUNT(t.transaction_id) as order_count, SUM(p.price) as total_spent
        FROM customers c
        INNER JOIN transactions t ON c.customer_id = t.customer_id
        INNER JOIN products p ON t.product_id = p.product_id
        GROUP BY c.name
        HAVING total_spent > 10000.00;
    """
    fraudsters = cursor.execute(fraud_query).fetchall()
    
    if not fraudsters:
        print("- System Clear. No fraudulent spending detected.")
    else:
        for f in fraudsters:
            print(f"- ACCOUNT FROZEN: {f[0]} made {f[1]} rapid orders totaling ${f[2]:,.2f}!")

print("\nReport Generation Complete.")