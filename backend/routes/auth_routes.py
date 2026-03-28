from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import re
import mysql.connector
from config.settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

auth_bp = Blueprint("auth", __name__)

# ----------------------
# 🔹 MySQL DB Helper
# ----------------------
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# ----------------------
# 🔍 Validation Helpers
# ----------------------
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_age(age):
    try:
        age = int(age)
        return 1 <= age <= 120
    except:
        return False

def is_strong_password(password):
    return len(password) >= 6

# ----------------------
# 📝 REGISTER
# ----------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required = ["name", "email", "password", "age", "gender", "role"]

    # Validate presence
    if not data or not all(field in data and data[field] for field in required):
        return jsonify({"error": "All fields are required"}), 400

    # Validate email, age, password
    if not is_valid_email(data["email"]):
        return jsonify({"error": "Invalid email format"}), 400
    if not is_valid_age(data["age"]):
        return jsonify({"error": "Invalid age"}), 400
    if not is_strong_password(data["password"]):
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    hashed_password = generate_password_hash(data["password"])

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check for duplicate email
        cursor.execute("SELECT * FROM users WHERE email=%s", (data["email"],))
        if cursor.fetchone():
            return jsonify({"error": "Email already exists"}), 409

        # Insert new user
        cursor.execute(
            "INSERT INTO users (name, email, password, age, gender, role) VALUES (%s,%s,%s,%s,%s,%s)",
            (data["name"], data["email"], hashed_password, data["age"], data["gender"], data["role"])
        )
        conn.commit()

        return jsonify({"message": "Registration successful"}), 201

    except mysql.connector.Error as e:
        return jsonify({"error": f"MySQL Error: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()

# ----------------------
# 🔑 LOGIN
# ----------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (data["email"],))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], data["password"]):
            token = create_access_token(identity=user["email"])
            return jsonify({
                "message": "Login successful",
                "token": token,
                "role": user["role"],
                "name": user["name"]
            }), 200

        return jsonify({"error": "Invalid credentials"}), 401

    except mysql.connector.Error as e:
        return jsonify({"error": f"MySQL Error: {str(e)}"}), 500

    finally:
        cursor.close()
        conn.close()