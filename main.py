from fastapi import FastAPI, HTTPException
from typing import List
from models import User, init_db, get_all_users, get_user_by_id, add_user

app = FastAPI()

init_db()

@app.get("/users", response_model=List[User])
def get_users():
    return get_all_users()

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/create_user", response_model=User)
def create_user(user: User):
    try:
        add_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user
