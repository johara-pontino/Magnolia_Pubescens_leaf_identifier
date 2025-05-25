from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
import numpy as np

def load_model():
    # Make sure your model path is correct relative to this file or absolute path
    model_path = "./resnet50_nilo.h5"
    model = keras_load_model(model_path)
    return model

def predict_image(model, image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array)
    print("Raw prediction output:", prediction)  # For debugging purposes
    # Assuming binary classification: output is a probability
    return int(prediction[0][0] > 0.5)
