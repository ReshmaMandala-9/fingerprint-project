import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 🔐 App security
SECRET_KEY = "fingerprint-secret-key"
JWT_SECRET_KEY = "jwt-secret-key-change-this"

# 📁 File upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024   # 5MB limit

# 💾 MySQL Database settings
MYSQL_HOST = "localhost"
MYSQL_USER = "root"       # Change to your DB user
MYSQL_PASSWORD = "23BQ1A05D2"   # Change to your DB password
MYSQL_DB = "fingerprint_db"