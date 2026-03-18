from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import time

app = FastAPI(title="FastAPI Assignment", version="1.0.0")

START_TIME = time.time()

# ----- Models -----
class UserCreate(BaseModel):
    name: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str

# ----- Mock DB -----
USERS = [
    {"id": 1, "name": "Alice",   "email": "alice@example.com"},
    {"id": 2, "name": "Bob",     "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]

# ----- Routes -----
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "uptime": round(time.time() - START_TIME, 2),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/users")
def get_users():
    return {"success": True, "data": USERS}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    user = next((u for u in USERS if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": user}

@app.post("/api/users", status_code=201)
def create_user(user: UserCreate):
    new_user = {"id": len(USERS) + 1, "name": user.name, "email": user.email}
    USERS.append(new_user)
    return {"success": True, "data": new_user, "message": "User created"}
