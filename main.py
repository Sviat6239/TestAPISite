from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI()

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

init_db()

@app.get("/users", response_model=List[User])
def get_users():
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users")
    users = [User(**dict(row)) for row in cursor.fetchall()]
    conn.close()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**dict(user))

@app.post("/create_user", response_model=User)
def create_user(user: User):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (id, username, email) VALUES (?, ?, ?)",
            (user.id, user.username, user.email),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=400, detail="User with this email already exists")
    conn.close()
    return user
