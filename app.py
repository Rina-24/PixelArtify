from flask import Flask, render_template, request, send_from_directory
import cv2
import os
import numpy as np
from make_transparent import make_transparent
from img_change import mosaic, decreaseColor

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        # Save uploaded image
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.' + request.form['file_format'])
        file.save(filename)

        # Load and process the image
        img = cv2.imread(filename)
        pixel_size = int(request.form['pixel_size'])
        alpha = pixel_size / 100.0

        # Check file format and perform appropriate processing
        if request.form['file_format'] == 'jpg':
            mosaic_img = mosaic(img, alpha)
            dc_img = decreaseColor(mosaic_img)
        elif request.form['file_format'] == 'png':
            img_with_alpha = make_transparent(img, (255, 255, 255))
            mosaic_img = mosaic(img_with_alpha, alpha)
            dc_img = decreaseColor(mosaic_img)

        result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.' + request.form['file_format'])
        cv2.imwrite(result_filename, dc_img)

        return send_from_directory(app.config['UPLOAD_FOLDER'], 'result_image.' + request.form['file_format'])

if __name__ == '__main__':
    app.run(debug=True)
