from flask import Blueprint, request, jsonify
import os
from datetime import datetime

capture_bp = Blueprint("capture", __name__)

DATASET_PATH = "dataset/train"   # inside backend/

@capture_bp.route("/capture", methods=["POST"])
def capture():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    blood_group = request.form.get("blood_group")

    if not blood_group:
        return jsonify({"error": "Blood group missing"}), 400

    # Create folder if not exists
    save_dir = os.path.join(DATASET_PATH, blood_group)
    os.makedirs(save_dir, exist_ok=True)

    # Save file with timestamp
    filename = f"{blood_group}_{datetime.now().timestamp()}.png"
    save_path = os.path.join(save_dir, filename)
    image.save(save_path)

    return jsonify({
        "message": f"Saved to {save_dir}",
        "file": filename
    }), 200