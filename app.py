# app.py
from flask import Flask, render_template, request, send_from_directory
import cv2
import os
import numpy as np
from make_transparent import make_transparent

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def mosaic(img, alpha):
    h, w, ch = img.shape
    img = cv2.resize(img, (int(w * alpha), int(h * alpha)))
    img = cv2.resize(img, (w, h), interpolation=cv2.INTER_NEAREST)
    return img

def decreaseColor(img):
    dst = img.copy()
    for i in range(1, 8):
        idx = np.where((32 * i <= img) & (32 * (i + 1) > img))
        dst[idx] = 32 * i + 16
    return dst

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
        mosaic_img = mosaic(img,alpha)
        dc_img = decreaseColor(mosaic_img)


        # Check file format and perform appropriate processing
        if request.form['file_format'] == 'jpg':
            result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.jpg')
            cv2.imwrite(result_filename, dc_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        elif request.form['file_format'] == 'png':
            dc_img_with_alpha = make_transparent(dc_img, (255, 255, 255))
            result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.png')
            cv2.imwrite(result_filename,  dc_img_with_alpha, [cv2.IMWRITE_PNG_COMPRESSION, 9])


        # Call make_transparent function from make_transparent.py
        # img_transparent = make_transparent(img, target_color=(255, 255, 255))

        # # Pixel processing
        # mosaic_img = mosaic(img_transparent,alpha)
        # dc_img = decreaseColor(mosaic_img)

        # # Save the processed image
        # result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.' + request.form['file_format'])
        # if request.form['file_format'] == 'jpg':
        #     cv2.imwrite(result_filename, dc_img, [cv2.IMWRITE_JPEG_QUALITY, 95])  # JPG形式で保存
        # elif request.form['file_format'] == 'png':
        #     cv2.imwrite(result_filename, dc_img, [cv2.IMWRITE_PNG_COMPRESSION, 9])  # PNG形式で保存
        # result_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'result_image.png')
        # cv2.imwrite(result_filename, dc_img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        return send_from_directory(app.config['UPLOAD_FOLDER'], 'result_image.' + request.form['file_format'])

if __name__ == '__main__':
    app.run(debug=True,use_debugger=True)
