import sqlite3

conn = sqlite3.connect('complaints.db')
cursor = conn.cursor()

# Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
''')

# Complaints Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    description TEXT,
    status TEXT
)
''')

# Default Admin
cursor.execute(
    "INSERT OR IGNORE INTO users(username, password, role) VALUES (?, ?, ?)",
    ("admin", "admin123", "admin")
)

conn.commit()
conn.close()

print("Database Created Successfully")