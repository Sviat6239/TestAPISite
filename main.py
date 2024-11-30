from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Модель користувача
class User(BaseModel):
    id: int
    username: str
    email: str

# Імітація бази даних
users = [
    User(id=1, username="user1", email="user1@example.com"),
    User(id=2, username="user2", email="user2@example.com"),
    User(id=3, username="user3", email="user3@example.com"),
]

# Ендпоінт для отримання списку всіх користувачів
@app.get("/users", response_model=List[User])
def get_users():
    return users

# Ендпоінт для отримання інформації про користувача за ID
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Ендпоінт для створення нового користувача
@app.post("/create_user", response_model=User)
def create_user(user: User):
    if any(existing_user.email == user.email for existing_user in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    users.append(user)
    return user
