from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import shutil
import os

app = FastAPI()

# Load model once at startup
model = keras_load_model("resnet50_nilo.h5")

@app.get("/")
def read_root():
    return {"message": "Magnolia Classifier API is live!"}

@app.post("/predict/")
async def classify_image(file: UploadFile = File(...)):
    try:
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        img = image.load_img(temp_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0

        prediction = model.predict(img_array)[0][0]
        os.remove(temp_path)  # Clean up

        predicted_label = "Nilo" if prediction > 0.5 else "Not Nilo"

        return JSONResponse({
            "class": predicted_label,
            "confidence": float(prediction)
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/submit/")
async def submit_image(file: UploadFile = File(...)):
    try:
        save_dir = "submitted_images"
        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(save_dir, file.filename)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": f"Image '{file.filename}' submitted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
