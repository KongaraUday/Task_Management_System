import sqlite3

def create_connection():
    """Create a database connection to SQLite database"""
    conn = sqlite3.connect("tasks.db")
    return conn

def create_table():
    """Create tasks table if it doesn't exist"""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            due_date TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

# Run when file is executed
if __name__ == "__main__":
    create_table()