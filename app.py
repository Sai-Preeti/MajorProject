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

@app.route('/predict', methods=['GET', 'POST'])
def predict():
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
        return render_template('predict.html', filename=filename)
    return render_template('predict.html')
            # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
@app.route('/result', methods=['POST'])
def result():
    # Add your prediction logic here
    return render_template('prediction.html')

@app.route('/', methods=['GET','POST'])
def index():
    # Add your prediction logic here
    return render_template('index.html')

# import requests
# from geopy.geocoders import Nominatim

# def get_lat_long(location_name):
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     location = geolocator.geocode(location_name)
#     if location:
#         return location.latitude, location.longitude
#     else:
#         return None, None

# def find_pulmonologists_nearby(api_key, location):
#     url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#     params = {
#         "key": api_key,
#         "location": location,
#         "radius": 5000,  # You can adjust the radius as needed
#         "keyword": "pulmonologist"
#     }
#     response = requests.get(url, params=params)
#     results = response.json().get("results", [])
#     return results

# # Example usage
# api_key = "YOUR_API_KEY"  # Replace with your actual API key
# location_name = "Your location name"  # Replace with your actual location name
# latitude, longitude = get_lat_long(location_name)
# if latitude is not None and longitude is not None:
#     location = f"{latitude},{longitude}"
#     pulmonologists = find_pulmonologists_nearby(api_key, location)
#     for pulmonologist in pulmonologists:
#         print(pulmonologist["name"], pulmonologist["vicinity"])
# else:
#     print("Location not found.")

import requests

def get_lat_long(location_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "state": location_name,  # Specify state name
        "format": "json",
        "country": "India",  # Specify country
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("API Response:", data)  # Print the response for debugging
    if data:
        # Check if the data list is not empty
        first_result = data[0]
        latitude = first_result.get("lat")
        longitude = first_result.get("lon")
        if latitude is not None and longitude is not None:
            return latitude, longitude
    # If data list is empty or latitude/longitude is None
    return None, None

def find_pulmonologists_nearby(location):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": "pulmonologist",
        "format": "json",
        "lat": location[0],
        "lon": location[1],
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Example usage
location_name = "Vasavi, India"  # Replace with the actual location name in India
latitude, longitude = get_lat_long(location_name)
if latitude is not None and longitude is not None:
    location = (latitude, longitude)
    pulmonologists = find_pulmonologists_nearby(location)
    if pulmonologists:
        for pulmonologist in pulmonologists:
            print(pulmonologist["display_name"])
    else:
        print("No pulmonologists found near the specified location.")
else:
    print("Location not found.")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print("Im here")
    print(send_from_directory(app.config['UPLOAD_FOLDER'], filename))
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/what_is_emphysema')
def what_is_emphysema():
    return render_template('what_is_emphysema.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nearme')
def nearme():
    return render_template('near_me.html')
    
if __name__ == '__main__':
    app.run(debug=True)
