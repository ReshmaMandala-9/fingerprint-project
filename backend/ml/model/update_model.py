from tensorflow.keras.models import load_model

old_model_path = "fingerprint_model.h5"
new_model_path_h5 = "fingerprint_model_updated.h5"
new_model_path_tf = "fingerprint_model_savedmodel"
try:
    # Load the old model
    old_model = load_model(old_model_path)
    print(f"Old model loaded successfully from {old_model_path}")

    # Save in updated H5 format
    old_model.save(new_model_path_h5, save_format="h5")
    print(f"Model re-saved in H5 format at {new_model_path_h5}")

    # Optionally, save in TensorFlow SavedModel format (recommended)
    old_model.save(new_model_path_tf)
    print(f"Model also saved in SavedModel format at {new_model_path_tf}")

except Exception as e:
    print(f"Error updating model: {e}")