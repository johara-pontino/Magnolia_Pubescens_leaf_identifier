import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.backend import clear_session
import numpy as np
import io
from datetime import datetime

app = FastAPI()

# Allow cross-origin requests from Vercel or local development
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

# === MODEL CONFIGURATION ===
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "resnet50_nilo.h5")
MODEL_URL = "https://drive.google.com/uc?export=download&id=18kZjv_7XU2nGW6UmIy0fRnKeJEXrWgMy"
label_map = {0: "Nilo", 1: "Not Nilo"}

model = None

def download_model_if_needed():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_DIR, exist_ok=True)
        print("Downloading model from Google Drive...")
        try:
            response = requests.get(MODEL_URL)
            response.raise_for_status()
            with open(MODEL_PATH, "wb") as f:
                f.write(response.content)
            print("Model downloaded successfully.")
        except Exception as e:
            print("Failed to download model:", e)
            raise RuntimeError("Model download failed.")

@app.on_event("startup")
def load_model_on_startup():
    global model
    download_model_if_needed()
    model = load_model(MODEL_PATH)
    print("✅ Model loaded and ready.")

# === ROUTES ===

@app.get("/")
def read_root():
    return {"message": "API is running on Railway!"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid image file")

    contents = await file.read()
    try:
        img = image.load_img(io.BytesIO(contents), target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        prediction = model.predict(img_array)[0][0]
        label = label_map[int(prediction > 0.5)]

        return JSONResponse({
            "label": label,
            "probability": float(prediction)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed")
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
        return {"message": "Image submitted.", "filename": filename}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save image")
