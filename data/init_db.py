import sqlite3
import os
import datetime

# Get path to the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
print(f"Creating database at {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    status TEXT
)
""")

# Create waste metrics table
cursor.execute("""
CREATE TABLE IF NOT EXISTS waste_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    volume INTEGER,
    cleanliness_score INTEGER
)
""")

# Create rewards table
cursor.execute("""
CREATE TABLE IF NOT EXISTS rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    points INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

# Add a demo user if it doesn't exist
cursor.execute("SELECT id FROM users WHERE username = 'demo'")
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password, status) VALUES (?, ?, ?)",
                  ("demo", "password", "active"))
    print("Demo user added")
    
    # Get the user id
    cursor.execute("SELECT id FROM users WHERE username = 'demo'")
    user_id = cursor.fetchone()[0]
    
    # Add points for the demo user
    cursor.execute("INSERT INTO rewards (user_id, points) VALUES (?, ?)", 
                  (user_id, 120))
    print("Demo rewards added")

# Add mock waste metrics data for the past 7 days
cursor.execute("DELETE FROM waste_metrics")  # Clear existing data
today = datetime.datetime.now()
for i in range(7, 0, -1):
    date = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
    volume = 35 + (i % 3) * 5  # Generate some variation
    cleanliness_score = 80 + (i % 3) * 5
    cursor.execute("INSERT INTO waste_metrics (date, volume, cleanliness_score) VALUES (?, ?, ?)",
                 (date, volume, cleanliness_score))
print("Mock waste metrics data added")

conn.commit()
conn.close()
print("Database initialized successfully")