import sqlite3
from pathlib import Path

current_dir = Path(__file__).resolve().parent
db_path = current_dir / "user.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Reading Database...")
cursor.execute("SELECT * FROM users")

all_users=cursor.fetchall()
for user in all_users:
    print(f"ID: {user[0]}, First Name: {user[1]}, Last Name: {user[2]}, Email: {user[3]}, Role: {user[4]}, Balance: {user[5]}")
    
print("\nUpdating a new user...")

update_query = "UPDATE users SET account_balance = ? WHERE first_name = ?"
cursor.execute(update_query,(2500, 'Chill'))
conn.commit()
print("Updated user Successfully")

delete_query = "DELETE FROM users WHERE first_name = ?"
cursor.execute(delete_query,('Elon',))
conn.commit()
print("Deleted user Successfully")

print("\nReading Database after update and delete...")
cursor.execute("SELECT * FROM users")
all_users=cursor.fetchall()
for user in all_users:
    print(f"ID: {user[0]}, First Name: {user[1]}, Last Name: {user[2]}, Email: {user[3]}, Role: {user[4]}, Balance: {user[5]}")
conn.close()