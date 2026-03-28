from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import socket
import os

# Import your settings and blueprints
from config.settings import SECRET_KEY, JWT_SECRET_KEY, UPLOAD_FOLDER
from routes.auth_routes import auth_bp
from routes.predict_routes import predict_bp
from routes.capture_routes import capture_bp
from ml import predictor

app = Flask(__name__)

# 🔐 Security configs
app.config["SECRET_KEY"] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Enable JWT
jwt = JWTManager(app)

# Enable CORS
CORS(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(predict_bp, url_prefix="/api")
app.register_blueprint(capture_bp, url_prefix="/api")

# Load the ML model at startup
print("🔹 Loading ML model...")
try:
    predictor.load_model_if_not_loaded()  # you can define this function in predictor.py
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"⚠ Could not load model: {e}")

# Home route
@app.route("/")
def home():
    return jsonify({
        "message": "Secure Backend Running",
        "security": "JWT + File Protection Enabled"
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# Run the app safely on a free port
if __name__ == "__main__":
    DEFAULT_PORT = 5000

    def find_free_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", DEFAULT_PORT))
            PORT = DEFAULT_PORT
    except OSError:
        PORT = find_free_port()

    print(f"⚡ Running Secure Backend on http://127.0.0.1:{PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)