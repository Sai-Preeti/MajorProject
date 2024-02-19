from flask import Flask, render_template, request,redirect,  url_for, send_from_directory
import requests
import random
import os

app = Flask(__name__,template_folder='templates')

app.static_folder = 'static'
app.static_url_path = '/static'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return render_template('index.html', filename=filename)
            # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Add your prediction logic here
    return render_template('prediction.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("Im here")
    print(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
    app.run(debug=True)
