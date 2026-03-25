from fastapi import FastAPI, HTTPException
from models import User
import json
from typing import Optional

app = FastAPI()

FILE_NAME = "users.json"


# -------- Helper Functions -------- #

def read_users():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []


def write_users(users):
    with open(FILE_NAME, "w") as file:
        json.dump(users, file, indent=4)


# -------- Endpoints -------- #

# ✅ GET /users (search + sort)
@app.get("/users")
def get_users(search: Optional[str] = None, sort: Optional[str] = None, order: str = "asc"):
    users = read_users()

    # Search
    if search:
        users = [u for u in users if search.lower() in u["name"].lower()]

    # Sort
    if sort:
        reverse = True if order == "desc" else False
        users = sorted(users, key=lambda x: x.get(sort, ""), reverse=reverse)

    return users


# ✅ GET /users/{id}
@app.get("/users/{user_id}")
def get_user(user_id: int):
    users = read_users()

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


# ✅ POST /users
@app.post("/users")
def create_user(user: User):
    users = read_users()

    new_id = 1 if not users else max(u["id"] for u in users) + 1
    user_dict = user.dict()
    user_dict["id"] = new_id

    users.append(user_dict)
    write_users(users)

    return {"message": "User created", "user": user_dict}


# ✅ PUT /users/{id}
@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    users = read_users()

    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i].update(updated_user.dict(exclude_unset=True))
            users[i]["id"] = user_id

            write_users(users)
            return {"message": "User updated", "user": users[i]}

    raise HTTPException(status_code=404, detail="User not found")


# ✅ DELETE /users/{id}
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    users = read_users()

    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            write_users(users)
            return {"message": "User deleted"}

    raise HTTPException(status_code=404, detail="User not found")