# here we define the tables of our database

from flask_login import UserMixin # library for better user handling
from . import db

# table for the users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=True, unique=True) # as connect possibility
    password = db.Column(db.String(250), nullable=True)
    type = db.Column(db.Boolean, nullable=True) # True for providers, False for customers

    preferences = db.relationship('Preferences', backref='user', lazy=True)
    matches = db.relationship('Matches', backref='user', lazy=True)
    offer = db.relationship('Offer', backref='user', lazy=True)

# table for the preferences
class Preferences(db.Model):
    __tablename__ = 'preferences'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ...
    # add some parameters and keys

# tables for the matches
class Matches(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    # user matched with offer
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    # the matching score between the users and between the user and the offer
    score = db.Column(db.Float, nullable=True)
    successful_match = db.Column(db.Boolean, nullable=True) # True if successful

# tables for the flat offers
# for MVP pre configured (+ provider accounts)
class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    time_live = db.Column(db.DateTime, nullable=True)

    matches = db.relationship('Matches', backref='offer', lazy=True)

# further tables
# ...

