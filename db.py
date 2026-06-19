import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    age_group TEXT,
    current_stage INTEGER DEFAULT 1,
    inventory TEXT DEFAULT '',
    score INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    age_group TEXT,
    stage INTEGER,
    stars INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()

def get_user_by_name(name):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,name,age_group,current_stage,inventory,score FROM users WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "age_group": row[2], "current_stage": row[3], "inventory": row[4], "score": row[5]}
    return None

def create_user(name, age_group):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users(name,age_group,current_stage,inventory,score) VALUES(?,?,?,?,?)",
                (name, age_group, 1, "", 0))
    conn.commit()
    user = get_user_by_name(name)
    conn.close()
    return user

def update_user_progress(user_id, stage, add_score=0, add_inventory=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET current_stage=?, score=score+? WHERE id=?", (stage, add_score, user_id))
    if add_inventory:
        cur.execute("SELECT inventory FROM users WHERE id=?", (user_id,))
        inv = cur.fetchone()[0] or ""
        new = (inv + "," + add_inventory).strip(",")
        cur.execute("UPDATE users SET inventory=? WHERE id=?", (new, user_id))
    conn.commit()
    conn.close()

def log_progress(user_id, age_group, stage, stars):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO progress(user_id,age_group,stage,stars) VALUES(?,?,?,?)", (user_id, age_group, stage, stars))
    conn.commit()
    conn.close()
