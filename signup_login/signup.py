from flask import render_template, redirect, request
from werkzeug.security import generate_password_hash
import re
import json

from db_config import db
from db_config.db_tables import FlatMate, Preferences, Offer

# Signup Handler class
class Signup:
    def __init__(self, first_name: str, email: str, password: str, password_confirmation: str, preferences: dict, apartment: dict, type: bool) -> None:
        self.first_name = first_name
        self.email = email
        self.password = password
        self.password_confirmation = password_confirmation
        self.preferences = preferences
        self.apartment = apartment
        self.type = True if type == 'true' else False
        self.error = ''

    # method to check the email validity
    def email_check(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.error = "Invalid email address."
        return self.error

    # method to check the password validity
    def password_check(self):
        # password too short
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
        try:
            # transform a dictionary in kwargs value pairs
            for key, item in self.preferences.items():
                if key in ['age', 'community', 'semester']:
                    self.preferences[key] = int(item)
                elif key == 'language':
                    self.preferences[key] = str(item)
                else:
                    self.preferences[key] = True if item == 'true' else False
            
            # add the user_id to the preferences
            self.preferences['user_id'] = FlatMate.query.filter_by(email=self.email).first().id

            # create a new preference instance
            new_preference = Preferences(**self.preferences)

            # add them to the database
            db.session.add(new_preference)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            self.error = f"An error occurred while adding preferences: {str(e)}"

    # add apartment details
    def add_apartment(self):
        try:
            # transform a dictionary in kwargs value pairs
            for key, item in self.apartment.items():
                if key in ['title', 'description', 'address']:
                    self.apartment[key] = str(item)
                elif key in ['price', 'distance']:
                    self.apartment[key] = float(item)
                else:
                    self.apartment[key] = int(item)
            
            # add the user_id to the apartment
            self.apartment['user_id'] = FlatMate.query.filter_by(email=self.email).first().id

            # create a new preference instance
            new_apartment = Offer(**self.apartment)

            # add them to the database
            db.session.add(new_apartment)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            self.error = f"An error occurred while adding apartment details: {str(e)}"
    
    # create a new user
    def new_user(self):
        try:
            # create a password hash for security reasons
            hashed_password = generate_password_hash(self.password)
            # there is already a user with this email registered in the system
            if FlatMate.query.filter_by(email=self.email).first():
                self.error = 'There is already a user with this email registered.'
                return render_template('signup.html', error=self.error)
            else:
                # create a new user and move on to the dashboard
                new_user = FlatMate(first_name=self.first_name, email=self.email, password=hashed_password, type=self.type)
                # add the new entry to the database
                db.session.add(new_user)
                db.session.commit()
                # add the preferences
                self.add_preferences()
                # if provider add the apartment details
                if self.type:
                    self.add_apartment()
                # error handling
                if self.error:
                    return render_template('signup.html', error=self.error)
                # if provider
                if self.type:
                    return redirect('/provider_dashboard')
                # if customer
                else:
                    return redirect('/customer_dashboard')
        except Exception as e:
            db.session.rollback()
            self.error = f"An error occurred while creating a new user: {str(e)}"
            return render_template('signup.html', error=self.error)

# the signup function
def signup_1(request):
    error = ''
    # check whether there is a POST request, otherwise only a page load 'signup.html'
    if request.method == 'POST':
        # check whether all required fields are filled
        if request.form.get("first_name") and request.form.get("email") and request.form.get("password") and request.form.get("password_confirmation") and request.form.get("type"):
            try:
                attributes = {}
                attributes['pets'] = request.form.get("attributes[pets]")
                attributes['smoking'] = request.form.get("attributes[smoking]")
                attributes['sex'] = request.form.get("attributes[sex]")
                attributes['age'] = request.form.get("attributes[age]")
                attributes['relationship_status'] = request.form.get("attributes[relationship_status]")
                attributes['degree'] = request.form.get("attributes[degree]")
                attributes['language'] = request.form.get("attributes[language]")
                attributes['community'] = request.form.get("attributes[community]")
                attributes['attendance'] = request.form.get("attributes[attendance]")
                attributes['semester'] = request.form.get("attributes[semester]")
                attributes['fitness'] = request.form.get("attributes[fitness]")
                preferences = attributes

                type = request.form.get("type")
                if type == 'true':
                    apartment = {}
                    apartment['title'] = request.form.get("apartment[title]")
                    apartment['description'] = request.form.get("apartment[description]")
                    apartment['address'] = request.form.get("apartment[address]")
                    apartment['price'] = request.form.get("apartment[price]")
                    apartment['distance'] = request.form.get("apartment[distance]")
                    apartment['apartment_size'] = request.form.get("apartment[apartment_size]")
                    apartment['room_size'] = request.form.get("apartment[room_size]")
                    apartment['roommates'] = request.form.get("apartment[roommates]")
                    apartment['bathrooms'] = request.form.get("apartment[bathrooms]")
                else:
                    apartment = {}

            except (ValueError, TypeError) as e:
                return render_template('signup.html', error="Invalid preferences or type format.")
            
            # initialize a signup instance
            signup_instance = Signup(request.form.get("first_name"), request.form.get("email"), request.form.get("password"), request.form.get("password_confirmation"), preferences, apartment, type)
            
            # check the email validity
            error = signup_instance.email_check()
            if error:
                return render_template('signup.html', error=error)
            
            # check the password validity
            error = signup_instance.password_check()
            # if the password is valid, create a new user, else return the signup page with an error
            if error == '':
                return signup_instance.new_user()
            else:
                return render_template('signup.html', error=error)
        else:
            error = 'Fill in all required fields'
    return render_template('signup.html', error=error)