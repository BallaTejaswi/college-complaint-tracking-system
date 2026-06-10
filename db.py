import sqlite3

conn = sqlite3.connect('complaints.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    description TEXT,
    status TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")