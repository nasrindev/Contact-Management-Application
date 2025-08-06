import sqlite3

conn = sqlite3.connect('contacts.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    address TEXT,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")