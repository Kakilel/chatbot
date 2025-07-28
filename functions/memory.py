import sqlite3
import os
import re

DB_PATH = "data/memory.db"

def init_memory():
    """
    Ensure the memory DB and table exists.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL
            )
        ''')

def remember(key: str, value: str) -> str:
    """
    Store a key-value memory.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO memory (key, value) VALUES (?, ?)", (key.lower(), value))
    return f"I’ll remember that {key} is {value}."

def recall(key: str) -> str:
    """
    Retrieve a memory value by key (partial match supported).
    """
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT value FROM memory WHERE key LIKE ?", (f"%{key.lower()}%",)).fetchone()
    return row[0] if row else "I don’t remember that."

def forget(key: str) -> str:
    """
    Forget a memory by key.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("DELETE FROM memory WHERE key LIKE ?", (f"%{key.lower()}%",))
        deleted = cursor.rowcount
    return "🗑️ Forgotten." if deleted else "I wasn’t remembering that."

def list_memory() -> dict:
    """
    List all stored memories as a dict.
    """
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT key, value FROM memory").fetchall()
    return {k: v for k, v in rows}

def handle_memory_command(text: str) -> str:
    """
    Natural language command interface for memory actions.
    """
    remember_match = re.match(r"(remember|note) that (.+?) is (.+)", text, re.I)
    forget_match = re.match(r"(forget|remove) (.+)", text, re.I)
    recall_match = re.match(r"(what|who|where|when|do you know|tell me about) (.+)", text, re.I)

    if remember_match:
        return remember(remember_match.group(2).strip(), remember_match.group(3).strip())
    elif forget_match:
        return forget(forget_match.group(2).strip())
    elif recall_match:
        return recall(recall_match.group(2).strip())
    return "I’m not sure what to do with that memory command."
