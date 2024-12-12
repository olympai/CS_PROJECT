import os
from flask import jsonify
from PIL import Image

ALLOWED_EXTENSIONS = {'png'}
UPLOAD_FOLDER = 'static/uploads'

# allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload file
def upload_file(file, id: int, type: str):
    if not file:
        return 'No file part', 400

    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename = f'{type}_{id}.png'
        
        # Generate storage path
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save file
        file.save(filepath)

        # (Optional) Validate the content, e.g., check if it is really an image
        try:
            with Image.open(filepath) as img:
                img.verify()  # Checks if it is a valid image
        except Exception:
            os.remove(filepath)  # Deletes the file if it is invalid
            return 'Uploaded file is not a valid image', 400

        return 'File uploaded successfully', 200
    else:
        return 'Invalid file type. Only .png allowed.', 400