from flask import Flask, render_template, request
import cv2
import numpy as np
import os
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image uploaded", 400

    image = request.files['image']

    # Save the uploaded image to disk
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # Read the saved image using OpenCV
    uploaded_image = cv2.imread(image_path)

    # Example: Convert the image to grayscale
    grayscale_image = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

    # Encode the processed image as base64
    retval, buffer = cv2.imencode('.jpg', grayscale_image)
    processed_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Encode the original image as base64
    retval, buffer = cv2.imencode('.jpg', uploaded_image)
    original_image_base64 = base64.b64encode(buffer).decode('utf-8')

    # Cleanup: Remove the uploaded image file from disk
    os.remove(image_path)

    return render_template('home.html', original_image_base64=original_image_base64, processed_image_base64=processed_image_base64)


if __name__ == "__main__":
    app.run(debug= True)