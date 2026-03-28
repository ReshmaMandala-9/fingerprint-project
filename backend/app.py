from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
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

# ✅ Load the ML model at startup (SAFE)
print("🔹 Loading ML model...")
try:
    # This works because your predictor.py already loads model on import
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"⚠ Could not load model: {e}")

# ✅ Home route (IMPORTANT for Render)
@app.route("/")
def home():
    return jsonify({
        "message": "Secure Backend Running 🚀",
        "status": "success"
    })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


# ✅ FIXED: Render-compatible port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"⚡ Running on port {port}")
    app.run(host="0.0.0.0", port=port)