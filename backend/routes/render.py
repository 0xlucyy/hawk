from app import app
from flask import Flask, request, render_template,jsonify

# import os
# APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')

@app.route("/")
def home():
    return render_template('index.html')
