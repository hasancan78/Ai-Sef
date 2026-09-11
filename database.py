import sqlite3
import uuid

DB_FILE = "ai_sef.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorites (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_favorite(content, category):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    fav_id = str(uuid.uuid4())
    cursor.execute("INSERT INTO favorites (id, content, category) VALUES (?, ?, ?)", (fav_id, content, category))
    conn.commit()
    conn.close()
    return fav_id

def remove_favorite(fav_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE id=?", (fav_id,))
    conn.commit()
    conn.close()

def get_favorites():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, category FROM favorites")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "text": row[1], "category": row[2]} for row in rows]

def update_category(fav_id, new_category):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE favorites SET category=? WHERE id=?", (new_category, fav_id))
    conn.commit()
    conn.close()
