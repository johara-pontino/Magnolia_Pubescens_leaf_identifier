import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import io
from datetime import datetime

app = FastAPI()


origins = [
    "http://localhost:3000",  # Local dev
    "https://magnolia-pubescens-leaf-identifier-6s7t-jaypontinos-projects.vercel.app",
    "https://magnolia-pubescens-leaf-identif-git-9900cb-jaypontinos-projects.vercel.app",
    "https://magnolia-pubescens-leaf-identifier-6s7t-hhkufosxa.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow frontend URLs here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def load_model_on_startup():
    global model
    model_path = "./resnet50_nilo.h5"
    model = keras_load_model(model_path)
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
    except Exception:
        raise HTTPException(status_code=400, detail="Error loading image")

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)[0][0]
    predicted_label = label_map[int(prediction > 0.5)]

    return JSONResponse({
        "label": predicted_label,
        "probability": float(prediction)
    })

@app.post("/submit/")
async def submit_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    contents = await file.read()

    # Ensure directory exists
    save_dir = "submitted_images"
    os.makedirs(save_dir, exist_ok=True)

    # Create a unique filename: timestamp + original filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S%f")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(save_dir, filename)

    try:
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save image")

    return JSONResponse({
        "message": "Image successfully submitted for future use.",
        "filename": filename
    })
