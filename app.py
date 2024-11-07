# this is the anchor file of our project, everything connects to this place
# it is the link between backend and frontend

from flask import render_template, request, session, redirect

from factory import app
from signup_login.login import login_1
from signup_login.signup import signup_1
from dashboard.dashboard import dashboard_1, dashboard_2, filtering_1, matches_1


# ROUTES

# this is our start route, it executes when the app is launched
@app.route('/')
def start():
    return render_template('index.html')

# the link in paranthesis is accessible from the frontend
@app.route('/index')
def index():
    return render_template('index.html')

# Signup
# FROM FRONTEND: POST (email, password, password_confirmation, preferences, type) type: bool -> provider (True) or customer (False)
# TO FRONTEND: signup.html, error
@app.route('/signup', methods=['POST'])
def signup():
    return signup_1(request)

# Login
# FROM FRONTEND: POST (email, password)
# TO FRONTEND: login.html, is_invalid
@app.route('/login', methods=['POST'])
def login():
    return login_1(request)

# Dashboard for customers
# TO FRONTEND: customer_dashboard.html, matchings
@app.route('/customer_dashboard', methods=['POST'])
def customer_dashboard():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return dashboard_1(user_id)

# Dashboard for providers
# TO FRONTEND: provider_dashboard.html, offers
@app.route('/provider_dashboard', methods=['POST'])
def provider_dashboard():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return dashboard_2(user_id)

# Filtering
# FROM FRONTEND: POST (criteria)
# TO FRONTEND: dashboard.html, matchings
@app.route('/filtering', methods=['POST'])
def filtering():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return filtering_1(user_id, request)

# Matches
# FROM FRONTEND: POST (offer_id)
# TO FRONTEND: dashboard.html, matchings, matched_contact
@app.route('/matches', methods=['POST'])
def matches():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return matches_1(user_id, request)
