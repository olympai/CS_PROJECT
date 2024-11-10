# login functionality

from flask import session, redirect, render_template
from werkzeug.security import check_password_hash

from db_config.db_tables import User

# the login function, takes the request as aparameter
def login_1(request):
    # check if there was a submit action, otherwise just a page load for the login page
    if request.method == 'POST':

        # get the information provided from the POST-request
        email = request.form.get('email')
        password = request.form.get('password')

        # get the user instance
        user = User.query.filter_by(email=email).first()

        # check whether there is such a user
        if user:
            # check the password
            if check_password_hash(user.password, password):
                # set the session id for this user
                session['user_id'] = user.id
                # go to the next page (now logged in)
                if user.type:
                    return redirect('/provider_dashboard')
                else:
                    return redirect('/customer_dashboard')

        # if the password is not valid or there is no such user account, return a warning, return to the login page
        is_invalid = True
        return render_template('login.html', is_invalid=is_invalid)
    return render_template('login.html')
