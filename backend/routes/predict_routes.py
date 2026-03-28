# predict_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os, uuid

from config.settings import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from ml.predictor import predict_for_user, predict_all_models

predict_bp = Blueprint("predict", __name__)


# 🔹 Allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    user_email = get_jwt_identity()

    # 🔥 Role from frontend (default = user)
    role = request.headers.get("Role", "user")

    print(f"[DEBUG] User: {user_email}, Role: {role}, Files: {list(request.files.keys())}")

    # 🔹 File key detection
    file_key = "file" if "file" in request.files else \
               "fingerprint_image" if "fingerprint_image" in request.files else None

    if not file_key:
        return jsonify({"error": "No file uploaded. Use key 'file' or 'fingerprint_image'"}), 400

    file = request.files[file_key]

    # 🔹 Validation
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}"}), 400

    # 🔹 File size check
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > MAX_FILE_SIZE:
        return jsonify({"error": f"File too large. Max size: {MAX_FILE_SIZE} bytes"}), 400
    file.seek(0)

    # 🔹 Save file
    filename = str(uuid.uuid4()) + "." + file.filename.rsplit(".", 1)[1].lower()
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # =========================
        # 👤 USER RESPONSE
        # =========================
        user_result = predict_for_user(filepath)

        # =========================
        # 🧪 RESEARCHER RESPONSE
        # =========================
        researcher_result = predict_all_models(filepath)

        # 🔥 Always return BOTH (simpler + avoids frontend issues)
        return jsonify({
            "message": "Prediction successful",
            "file": filename,
            "user": user_result,
            "researcher": researcher_result
        })

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        # 🔹 Cleanup
        if os.path.exists(filepath):
            os.remove(filepath)