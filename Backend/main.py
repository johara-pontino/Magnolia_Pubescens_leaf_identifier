from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import io

app = FastAPI()

# Load model once at startup
model = None
label_map = {0: "Nilo", 1: "Not Nilo"}

@app.on_event("startup")
def load_model_on_startup():
    global model
    model_path = "./resnet50_nilo.h5"
    model = keras_load_model(model_path)

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    contents = await file.read()
    try:
        img = image.load_img(io.BytesIO(contents), target_size=(224, 224))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error loading image")

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)  # Important! Use the same preprocessing as training

    prediction = model.predict(img_array)[0][0]
    predicted_label = label_map[int(prediction > 0.5)]

    return JSONResponse({
        "label": predicted_label,
        "probability": float(prediction)
    })
