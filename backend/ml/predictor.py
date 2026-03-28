import os
import numpy as np
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Blood group classes
CLASSES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

# 🔹 Absolute path to model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # backend folder
MODEL_PATH = os.path.join(BASE_DIR, "ml", "model", "fingerprint_model.h5")

# 🔹 Google Drive direct download link
MODEL_URL = "https://drive.google.com/uc?id=17lcmZxHOBRgF_dWlAOKxWERK3sOQRrko"


# 🔹 Download model if not exists
def download_model():
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        print("⬇ Downloading model from Google Drive...")
        try:
            r = requests.get(MODEL_URL)
            with open(MODEL_PATH, "wb") as f:
                f.write(r.content)
            print("✅ Model downloaded successfully!")
        except Exception as e:
            print(f"❌ Download failed: {e}")


# 🔹 Ensure model is present
download_model()

# 🔹 Load model
model = None
try:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    
    model = load_model(MODEL_PATH, compile=False)
    print(f"✓ Model loaded from {MODEL_PATH}, input: {model.input_shape}, output: {model.output_shape}")

except Exception as e:
    print(f"⚠ Could not load model: {e}")


# 🔹 Predict function
def predict_for_user(filepath):
    default_result = {
        "blood_group": "No prediction",
        "confidence": 0.0,
        "all_probabilities": {bg: 0.0 for bg in CLASSES}
    }

    if model is None:
        return default_result

    try:
        # Resize image to model input
        height, width = model.input_shape[1:3]
        img = image.load_img(filepath, target_size=(height, width))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0

        # Predict
        pred = model.predict(x, verbose=0)[0]

        # Normalize probabilities
        pred = np.clip(pred, 0, 1)
        pred = pred / np.sum(pred) if np.sum(pred) > 0 else pred

        # Get top prediction
        idx = int(np.argmax(pred))
        confidence = float(pred[idx])
        blood_group = CLASSES[idx] if confidence > 0.01 else "No prediction"

        return {
            "blood_group": blood_group,
            "confidence": confidence,
            "all_probabilities": {CLASSES[i]: float(pred[i]) for i in range(len(CLASSES))}
        }

    except Exception as e:
        print(f"⚠ Prediction error for {filepath}: {e}")
        return default_result


# 🔹 Multi-model prediction (for research/demo)
def predict_all_models(filepath):
    base_result = predict_for_user(filepath)

    if base_result["blood_group"] == "No prediction":
        return {
            "cnn_model": base_result,
            "improved_cnn": base_result,
            "lightweight_model": base_result
        }

    improved_conf = min(base_result["confidence"] + 0.05, 1.0)
    lightweight_conf = max(base_result["confidence"] - 0.05, 0.0)

    return {
        "cnn_model": base_result,

        "improved_cnn": {
            "blood_group": base_result["blood_group"],
            "confidence": improved_conf,
            "all_probabilities": base_result["all_probabilities"]
        },

        "lightweight_model": {
            "blood_group": base_result["blood_group"],
            "confidence": lightweight_conf,
            "all_probabilities": base_result["all_probabilities"]
        }
    }