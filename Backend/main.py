import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # disable GPU to avoid CUDA warnings


from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from model import load_model, predict_image
from utils import save_upload_file
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()

@app.post("/predict")
async def classify_leaf(file: UploadFile = File(...)):
    filepath = save_upload_file(file)
    prediction = predict_image(model, filepath)
    os.remove(filepath)
    return {"is_nilo": bool(prediction)}

@app.post("/submit-for-review")
async def submit_for_review(file: UploadFile = File(...)):
    os.makedirs("review_submissions", exist_ok=True)
    path = f"review_submissions/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "submitted", "path": path}