import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.backend import clear_session
import numpy as np
import io
from datetime import datetime

app = FastAPI()

# Allow frontend access (edit or add URLs if needed)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === MODEL CONFIGURATION ===
MODEL_PATH = os.path.join("Backend", "model", "resnet50_nilo.h5")
label_map = {0: "Nilo", 1: "Not Nilo"}

model = None

# Load model only when needed (lazy loading)
def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model not found at {MODEL_PATH}")
        print("Loading model from disk...")
        model = load_model(MODEL_PATH)
        print("✅ Model loaded.")
    return model

# === ROUTES ===

@app.get("/")
def read_root():
    return {"message": "API is running locally."}

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

        model = get_model()
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
