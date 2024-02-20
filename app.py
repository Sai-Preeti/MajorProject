from flask import Flask, render_template, request,redirect,  url_for, send_from_directory
from PIL import Image
import requests
import random
import os

app = Flask(__name__,template_folder='templates')

app.static_folder = 'static'
app.static_url_path = '/static'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def convert_tiff_to_png(file):
    try:
        # Open the TIFF image
        with Image.open(file.stream) as img:
            # Convert to RGB mode if not already in RGB mode
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Save as PNG format
            png_filename = file.filename.rsplit('.', 1)[0] + '.png'
            png_path = os.path.join(app.config['UPLOAD_FOLDER'], png_filename)
            img.save(png_path, format='PNG')
        print(f"Conversion successful: {file.filename} converted to {png_filename}")
        return png_filename
    except Exception as e:
        print(f"Error during conversion: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Ensure the file is an image
            if file.content_type.startswith('image'):
                # Convert TIFF to PNG
                filename = convert_tiff_to_png(file)
                if filename is None:
                    return "Error during conversion"
            else:
                return "Uploaded file is not an image"
        return render_template('index.html', filename=filename)
    return render_template('index.html')
            # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
@app.route('/predict', methods=['POST'])
def predict():
    # Add your prediction logic here
    return render_template('prediction.html')

@app.route('/test', methods=['GET','POST'])
def test():
    # Add your prediction logic here
    return render_template('test.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("Im here")
    print(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
    app.run(debug=True)
