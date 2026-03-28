import cv2
import numpy as np

def preprocess_image(image_path):

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        return None

    img = cv2.resize(img, (128,128))

    img = img / 255.0

    img = np.reshape(img,(1,128,128,1))

    return img