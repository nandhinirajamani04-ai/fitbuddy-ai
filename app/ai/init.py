def init_db():
    """Create database tables if they do not exist."""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Feedback table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            feedback TEXT NOT NULL
        )
    """)

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            weight REAL,
            goal TEXT,
            intensity TEXT,
            original_plan TEXT,
            updated_plan TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully")