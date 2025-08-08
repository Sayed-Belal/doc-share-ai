from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    ext = file.filename.rsplit('.', 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    file_url = f"https://doc-share-ai.onrender.com/file/{unique_name}"
    return jsonify({'url': file_url})

@app.route('/file/<filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
