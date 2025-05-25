import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # disable GPU to avoid CUDA warnings

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from model import load_model, predict_image
from utils import save_upload_file
import shutil
import os

app = FastAPI()

# Enable frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model once when the server starts
model = load_model()

@app.get("/")
async def root():
    return {"status": "API is running"}

@app.post("/predict")
async def classify_leaf(file: UploadFile = File(...)):
    # Save and classify image
    filepath = save_upload_file(file)
    prediction = predict_image(model, filepath)
    os.remove(filepath)
    return {"is_nilo": bool(prediction)}

@app.post("/submit-for-review")
async def submit_for_review(file: UploadFile = File(...)):
    # Save for manual review
    os.makedirs("review_submissions", exist_ok=True)
    save_path = f"review_submissions/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"status": "submitted", "filename": file.filename}
