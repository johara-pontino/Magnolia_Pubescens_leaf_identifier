import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.backend import clear_session
import numpy as np
import io
from datetime import datetime

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://magnolia-pubescens-leaf-identifier-6s7t-jaypontinos-projects.vercel.app",
    "https://magnolia-pubescens-leaf-identif-git-9900cb-jaypontinos-projects.vercel.app",
    "https://magnolia-pubescens-leaf-identifier-6s7t-hhkufosxa.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
label_map = {0: "Nilo", 1: "Not Nilo"}

MODEL_PATH = "./Backend/resnet50_nilo.h5"
# Google Drive direct download URL format (use "uc?export=download&id=" + file_id)
MODEL_DOWNLOAD_URL = "https://drive.google.com/uc?export=download&id=18kZjv_7XU2nGW6UmIy0fRnKeJEXrWgMy"

def download_model_if_missing():
    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found at {MODEL_PATH}, downloading from Google Drive...")
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        try:
            response = requests.get(MODEL_DOWNLOAD_URL)
            response.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            print("Model downloaded successfully.")
        except Exception as e:
            print(f"Failed to download model: {e}")
            raise RuntimeError("Cannot download model file")

@app.on_event("startup")
def load_model_on_startup():
    global model
    download_model_if_missing()
    model = keras_load_model(MODEL_PATH)
    print("Model loaded into memory.")

@app.get("/")
def read_root():
    return {"message": "API is running!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    contents = await file.read()
    try:
        img = image.load_img(io.BytesIO(contents), target_size=(224, 224))
    except Exception:
        raise HTTPException(status_code=400, detail="Error loading image")

    try:
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        prediction = model.predict(img_array)[0][0]
        predicted_label = label_map[int(prediction > 0.5)]

        return JSONResponse({
            "label": predicted_label,
            "probability": float(prediction)
        })
    finally:
        clear_session()

@app.post("/submit/")
async def submit_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    contents = await file.read()

    save_dir = "submitted_images"
    os.makedirs(save_dir, exist_ok=True)

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
