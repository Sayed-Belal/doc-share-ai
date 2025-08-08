from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    text = data['text'].strip()
    if not text:
        return jsonify({"error": "Empty text"}), 400

    filename = f"{uuid.uuid4()}.txt"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    file_url = f"{request.host_url}files/{filename}"
    return jsonify({"url": file_url})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    file_url = f"{request.host_url}files/{filename}"
    return jsonify({'url': file_url})

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
