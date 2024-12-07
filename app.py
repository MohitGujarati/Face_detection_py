import os
import cv2
import uuid
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Absolute paths to ensure correct file serving
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'processed_images')

# Ensure upload and output folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces_in_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    # Generate a unique filename
    output_filename = f"{uuid.uuid4()}_detected.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    
    # Save the image
    cv2.imwrite(output_path, img)
    
    return f'/processed_images/{output_filename}', len(faces)

@app.route('/FACE-DETECTION-WEB/processed_images/')
def serve_processed_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route('/api/detect-faces', methods=['POST'])
def process_images():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files')
    processed_images = []

    for file in files:
        # Secure the filename and save the uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Detect faces and save processed image
        output_path, num_faces = detect_faces_in_image(input_path)
        processed_images.append(output_path)
    
    return jsonify({
        'processed_images': processed_images,
        'message': f'Processed {len(files)} images'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)