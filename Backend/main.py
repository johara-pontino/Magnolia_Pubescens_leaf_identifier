import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # disable GPU to avoid CUDA warnings
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

def load_model():
    """Load and return the pre-trained Keras model from file."""
    model_path = "./resnet50_nilo.h5"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return keras_load_model(model_path)

def predict_image(model, image_path):
    """Predicts class of the image using the given model."""
    try:
        img = image.load_img(image_path, target_size=(224, 224))
    except Exception as e:
        raise ValueError(f"Error loading image {image_path}: {e}")

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize

    prediction = model.predict(img_array)[0][0]
    return {
        "class": int(prediction > 0.5),
        "confidence": float(prediction)
    }

