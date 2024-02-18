from flask import Flask, render_template, request,redirect, url_for
import requests
import random
import os

app = Flask(__name__,template_folder='templates')


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return render_template('preview.html', filename=filename)
    return redirect(request.url)

@app.route('/predict', methods=['POST'])
def predict():
    return 'Prediction page'

if __name__ == '__main__':
    app.run(debug=True)
