Here’s a detailed and visually appealing README file for your GitHub project:  

---

# **Face Detection Comparison**

Welcome to the **Face Detection Comparison** project! This web application allows users to upload images and compare original photos with their processed, face-detected counterparts using a backend API. The project features a responsive, user-friendly interface and showcases real-time progress tracking during the face detection process.

---

## **Table of Contents**

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Setup and Installation](#setup-and-installation)  
4. [How to Use](#how-to-use)  
5. [Output Example](#output-example)  
6. [Tech Stack](#tech-stack)  
7. [License](#license)  

---

## **Features**

- **Multiple Image Upload**: Upload up to 10 images simultaneously for face detection.  
- **Real-Time Progress Bar**: Displays progress while processing images.  
- **Responsive Design**: Works seamlessly on all devices.  
- **Side-by-Side Comparison**: View original and processed images side by side.  

---

## **Prerequisites**

Before running the project, ensure you have the following:  

- **Python** (Version 3.8 or above)  
- **Node.js** (For optional frontend modifications)  
- **Backend API**: A Python-based API for processing images (detailed below).  

---

## **Setup and Installation**

### **Frontend (HTML, CSS, JavaScript)**

1. Clone this repository:  
   ```bash
   git clone https://github.com/MohitGujarati/Face_detection_py.git
   cd face-detection-comparison
   ```

2. Open the `index.html` file in your browser or serve it locally using tools like Live Server.  

### **Backend (Python)**

1. Install required Python dependencies:  
   ```bash
   pip install flask flask-cors opencv-python
   ```

2. Set up a Flask API to process the images. Use the following Python script:(already done)

   ```python
   from flask import Flask, request, jsonify
   from flask_cors import CORS
   import cv2
   import os
   from werkzeug.utils import secure_filename

   app = Flask(__name__)
   CORS(app)

   UPLOAD_FOLDER = './uploads'
   PROCESSED_FOLDER = './processed'

   os.makedirs(UPLOAD_FOLDER, exist_ok=True)
   os.makedirs(PROCESSED_FOLDER, exist_ok=True)

   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

   @app.route('/api/detect-faces', methods=['POST'])
   def detect_faces():
       uploaded_files = request.files.getlist('files')
       processed_images = []

       for file in uploaded_files:
           filename = secure_filename(file.filename)
           filepath = os.path.join(UPLOAD_FOLDER, filename)
           file.save(filepath)

           # Perform face detection
           img = cv2.imread(filepath)
           gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
           face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
           faces = face_cascade.detectMultiScale(gray, 1.1, 4)

           for (x, y, w, h) in faces:
               cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

           processed_path = os.path.join(PROCESSED_FOLDER, filename)
           cv2.imwrite(processed_path, img)
           processed_images.append(f'/processed/{filename}')

       return jsonify({'processed_images': processed_images})

   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. Start the Flask server:  
   ```bash
   python app.py
   ```

4. Ensure the server is running at `http://localhost:5000`.

---

## **How to Use**

1. Open the **Face Detection Comparison** app in your browser.  
2. Click the **Choose Files** button and select 1-10 images.  
3. Press the **Start Face Detection** button to begin processing.  
4. View the original and processed images side by side in the comparison grid.  

---

## **Output Example**

Here’s an example of the output:  

![image](https://github.com/user-attachments/assets/55d03480-52d2-480b-bd78-decf44920487)


---

## **Tech Stack**

- **Frontend**: HTML5, CSS3, JavaScript  
- **Backend**: Python (Flask, OpenCV)  
- **Database (Optional)**: SQLite or other lightweight databases for storage  

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Contributors**

Feel free to contribute to this project! Open a pull request or create an issue for suggestions.  

---
