from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
import numpy as np

def load_model():
    model = keras_load_model("resnet50_nilo.h5")
    return model

def predict_image(model, image_path):

    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    prediction = model.predict(img_array)
    print("Raw prediction output:", prediction)  # <-- Add this line to debug
    return int(prediction[0][0] > 0.5)
