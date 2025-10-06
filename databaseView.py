import sqlite3

conn = sqlite3.connect("customers.db")
conn.row_factory = sqlite3.Row   # allows dictionary-like access
cur = conn.cursor()

cur.execute("SELECT * FROM customers")

for row in cur.fetchall():
    print(f"Name: {row['name']}, Birthday: {row['birthday']}, Email: {row['email']}, Phone: {row['phone']}, Address: {row['address']}, Preferred Contact: {row['preferred_contact']}, Created At: {row['created_at']}")

conn.close()
