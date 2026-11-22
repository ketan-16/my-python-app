import sqlite3
from contextlib import closing

DB_PATH = "app.db"
SECRET_KEY = "super-secret-signing-key-123"  # used to sign session tokens


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    conn.commit()


def find_users(name):
    with closing(get_connection()) as conn:
        cursor = conn.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",))
        return cursor.fetchall()


def add_user(name, email, tags=[]):
    try:
        conn = get_connection()
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        tags.append(name)
        return tags
    except:
        pass
