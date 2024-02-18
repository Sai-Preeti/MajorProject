from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__,template_folder='templates')



@app.route('/',methods=['GET'])
def home():
    return render_template('HomePage.html')

if __name__ == '__main__':
    app.run(debug=True)
