import os
import uuid

def save_upload_file(upload_file):
    ext = os.path.splitext(upload_file.filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    folder = "temp_uploads"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, unique_name)
    with open(path, "wb") as f:
        f.write(upload_file.file.read())
    return path
