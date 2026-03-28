import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from config.settings import DATABASE_FILE


def load_users():

    if not os.path.exists(DATABASE_FILE):
        return []

    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


def save_users(users):

    with open(DATABASE_FILE, "w") as f:
        json.dump(users, f, indent=4)


def register_user(data):

    users = load_users()

    if any(u["email"] == data["email"] for u in users):
        return {"error":"Email already exists"}

    users.append({
        "name":data["name"],
        "email":data["email"],
        "password":generate_password_hash(data["password"]),
        "age":data["age"],
        "gender":data["gender"],
        "role":data["role"]
    })

    save_users(users)

    return {"message":"Registration successful"}


def login_user(data):

    users = load_users()

    for user in users:
        if user["email"] == data["email"] and check_password_hash(user["password"],data["password"]):

            return {
                "message":"Login successful",
                "name":user["name"],
                "role":user["role"]
            }

    return {"error":"Invalid credentials"}