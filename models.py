import sqlite3
import os
from pydantic import BaseModel
from typing import List

# Модель користувача
class User(BaseModel):
    id: int
    username: str
    email: str

DB_PATH = "users.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        conn.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
            """
        )
        conn.commit()
        conn.close()

def get_all_users() -> List[User]:
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users")
    users = [User(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    return users

def get_user_by_id(user_id: int) -> User:
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return None
    return User(**dict(user))

def add_user(user: User):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (id, username, email) VALUES (?, ?, ?)",
            (user.id, user.username, user.email),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("User with this email already exists")
    conn.close()
