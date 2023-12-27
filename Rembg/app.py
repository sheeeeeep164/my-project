from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import os
from flask_cors import CORS
import shutil
app = Flask(__name__)
CORS(app)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload():
    if 'fileInput' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['fileInput']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file and allowed_file(file.filename):
        if not os.path.exists(INPUT_FOLDER):
            os.makedirs(INPUT_FOLDER)
        filename = os.path.join(INPUT_FOLDER, file.filename)
        file.save(filename)
        output_path = process_image(filename)
        return jsonify({'success': True, 'filename': output_path})
    else:
        return jsonify({'error': 'Invalid file type'})
@app.route('/output/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)
def process_image(input_path):
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)
    output_filename = 'result.png'  
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    command = ['python3', 'rembg-main/rembg.py', 'i', input_path, output_path]
    subprocess.run(command, check=True)
    return output_path
if __name__ == '__main__':
    app.run(debug=True)