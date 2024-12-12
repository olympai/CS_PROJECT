# this is the anchor file of our project, everything connects to this place
# it is the link between backend and frontend

from flask import render_template, request, session, redirect, json
from celery.result import AsyncResult

from factory import app
from signup_login.login import login_1
from signup_login.signup import signup_1
from dashboard.dashboard import dashboard_1, dashboard_2, filtering_1, matches_1, accept_1, reject_1, refresh_1
from celery_setup.celery_config import celery

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
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return signup_1(request)

# Login
# FROM FRONTEND: POST (email, password)
# TO FRONTEND: login.html, is_invalid
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_1(request)

# Logout
# TO FRONTEND: redirect to index.html
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')

# Dashboard for customers
# TO FRONTEND: customer_dashboard.html, matchings
@app.route('/customer_dashboard', methods=['GET', 'POST'])
def customer_dashboard():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return dashboard_1(user_id, 2)

# Clustering completed
@app.route('/clustering_completed', methods=['GET', 'POST'])
def clustering_completed():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    # load the customer dashboard with the respective matchings after clustering
    return dashboard_1(user_id, 2)

# Dashboard for providers
# TO FRONTEND: provider_dashboard.html, offers
@app.route('/provider_dashboard', methods=['GET', 'POST'])
def provider_dashboard():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return dashboard_2(user_id)

# Filtering
# FROM FRONTEND: POST (criteria)
# TO FRONTEND: customer_dashboard.html, matchings
@app.route('/filtering', methods=['GET', 'POST'])
def filtering():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return filtering_1(user_id, request)

# Matches
# FROM FRONTEND: POST (offer_id)
# TO FRONTEND: customer_dashboard.html, matchings, matched_contact
@app.route('/matches', methods=['GET', 'POST'])
def matches():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return matches_1(user_id, request)

# Refresh
# TO FRONTEND: customer_dashboard.html, matchings
@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return refresh_1(user_id)

# Accept from provider
@app.route('/provider_accept', methods=['GET', 'POST'])
def provider_accept():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return accept_1(user_id, request)

# Reject from provider
@app.route('/provider_reject', methods=['GET', 'POST'])
def provider_reject():
    # check the validity of the session
    if not session.get('user_id'):
        return redirect('/login')
    # get the user_id from the current flask session
    user_id = session.get('user_id')
    return reject_1(user_id, request)

@app.route('/progress')
def progress():
    if not session.get('user_id'):
        return render_template('login.html')
    jobid = request.values.get('jobid')
    if jobid:
        job = AsyncResult(jobid, app=celery)
        print(job.state)
        print(job.result)
        if job.state == 'PENDING':
            return json.dumps(dict(
                state=job.state,
                progress=0,
            ))
        elif job.state == 'PROGRESS':
            try:
                if job.result['total'] and job.result['current']:
                    pass
                else:
                    job.result['total']=1
                    job.result['current']=1
            except:
                return json.dumps(dict(
                    state=job.state,
                    progress=100,
                ))
            try:
                return json.dumps(dict(
                    state=job.state,
                    progress=(job.result['current'] * 1.0 / job.result['total'])*100,
                ))
            except:
                return json.dumps(dict(
                    state=job.state,
                    progress=100,
                ))
        elif job.state == 'SUCCESS':
            return json.dumps(dict(
                state=job.state,
                progress=100,
            ))
    return '{}'

# run the app
if __name__ == '__main__':
    app.run(debug=True)