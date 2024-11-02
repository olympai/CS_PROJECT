# this is the anchor file of our project, everything connects to this place
# it is the link between backend and frontend

from flask import render_template, session, redirect, request, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash

from factory import app


# ROUTES

# this is our start route, it executes if the app is loaded
@app.route('/')
def start():
    return render_template('index.html')

# the link in paranthesis is accessible from the frontend
@app.route('/index')
def index():
    return render_template('index.html')