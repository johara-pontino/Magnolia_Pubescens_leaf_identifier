import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # disable GPU to avoid CUDA warnings

from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

def load_model():
    """Loads and returns the trained Keras model."""
    return keras_load_model("resnet50_nilo.h5")

def predict_image(model, image_path):
    """
    Loads an image, processes it, and makes a binary classification prediction.
    Returns: {'class': 0 or 1, 'confidence': float}
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array)
    confidence = float(prediction[0][0])
    predicted_class = int(confidence > 0.5)
    print("Raw prediction output:", prediction)

    return {"class": predicted_class, "confidence": confidence}
