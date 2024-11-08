from flask import render_template, redirect
from werkzeug.security import generate_password_hash
import re

from db_config import db
from db_config.db_tables import User, Preferences

# Signup Handler class
class Signup:
    def __init__(self, email: str, password: str, password_confirmation: str, preferences: dict, type:bool) -> None:
        self.email = email
        self.password = password
        self.password_confirmation = password_confirmation
        self.preferences = preferences
        self.type = type
        self.error = ''

    # method to check the password validity
    def password_check(self):
        # password to short
        if len(self.password) < 8:
            self.error = "The password has to be at least eight characters long."
        # password does not contain a letter
        elif not re.search(r"[a-zA-Z]", self.password):
            self.error = "The password should contain at least one letter."
        # password does not contain a numeral
        elif not re.search(r"\d", self.password):
            self.error = "The password should contain at least one numeral."
        # password and password confirmation do not match
        elif self.password != self.password_confirmation:
            self.error = "Passwords should match."
        return self.error
    
    # add preferences
    def add_preferences(self):
        # transform a dictionary in kwargs value pairs
        new_preference = Preferences(**self.preferences)
        # add them to the database
        db.session.add(new_preference)
        db.session.commit()
    
    # create a new user
    def new_user(self):
        # create a password hash for security reasons
        hashed_password = generate_password_hash(self.password)
        # there is already a user with this email registered in the system
        if User.query.filter_by(email=self.email).first():
            self.error = 'There is already a user with this email registered.'
            return render_template('signup.html', error=self.error)
        else:
            # create a new user and move on to the dashboard
            new_user = User(email=self.email, password=hashed_password, type=self.type)
            # add the new entry to the database
            db.session.add(new_user)
            db.session.commit()
            # if provider
            if self.type:
                return redirect('/provider_dashboard')
            # if customer
            else:
                return redirect('/customer_dashboard')
        

# the signup function
def signup_1(request):
    error = ''
    # check whether there is a POST request, otherwise only a page load 'signup.html'
    if request.method == 'POST':
        # check whether all required fields are filled
        if request.form.get("email") and request.form.get("password") and request.form.get("password_confirmation") and request.form.get("preferences") and request.form.get("type"):
            # initialize a sihnup instance
            signup_instance = Signup(request.form.get("email"), request.form.get("password"), request.form.get("password_confirmation"), request.form.get("preferences"), request.form.get("type"))
            # check the password validity
            error = signup_instance.password_check()
            # if the password is valid, create a new user, else return the signup page with an error
            if error == '':
                signup_instance.add_preferences()
                signup_instance.new_user()
            else:
                return render_template('signup.html', error=error)
        else:
            error = 'Fill in all required fields'
    return render_template('signup.html', error)