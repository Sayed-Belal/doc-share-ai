from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import secrets
import string

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Random slug generator
def generate_slug(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.route('/upload', methods=['POST'])
def upload_text():
    text = request.form.get('content', '').strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    slug = generate_slug()
    filename = f"{slug}.txt"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

    file_url = request.host_url.rstrip('/') + '/files/' + filename
    return jsonify({"url": file_url})

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    slug = generate_slug()
    ext = os.path.splitext(file.filename)[1] or ''
    filename = f"{slug}{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    file_url = request.host_url.rstrip('/') + '/files/' + filename
    return jsonify({'url': file_url})

@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
