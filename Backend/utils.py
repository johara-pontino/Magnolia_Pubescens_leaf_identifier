import os
from uuid import uuid4

def save_upload_file(upload_file):
    filename = f"temp_{uuid4().hex}.jpg"
    file_path = f"temp/{filename}"
    os.makedirs("temp", exist_ok=True)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return file_path