import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image

from app import app

ALLOWED_EXTENSIONS = {'png'}

# allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload file
def upload_file(file, id: int, type: str):
    if not file:
        return jsonify({'error': 'No file part'}), 400

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename = f'{type}_{id}.png'
        
        # Generate storage path
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Create directory if it does not exist
        # os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save file
        file.save(filepath)

        # (Optional) Validate the content, e.g., check if it is really an image
        try:
            with Image.open(filepath) as img:
                img.verify()  # Checks if it is a valid image
        except Exception:
            os.remove(filepath)  # Deletes the file if it is invalid
            return jsonify({'error': 'Uploaded file is not a valid image'}), 400

        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    else:
        return jsonify({'error': 'Invalid file type'}), 400