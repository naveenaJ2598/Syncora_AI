
import sqlite3

DB_NAME = "syncora.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            transcript TEXT,
            summary TEXT,
            decisions TEXT,
            action_items TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_meeting(title, transcript, summary, decisions, action_items):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO meetings
        (title, transcript, summary, decisions, action_items)
        VALUES (?, ?, ?, ?, ?)
    """, (title, transcript, summary, decisions, action_items))

    conn.commit()
    conn.close()


def get_all_meetings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM meetings ORDER BY id DESC")
    meetings = cursor.fetchall()

    conn.close()
    return meetings
