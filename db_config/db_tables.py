# here we define the tables of our database

from flask_login import UserMixin # library for better flatmate handling
from . import db

# table for the users
class FlatMate(db.Model, UserMixin):
    __tablename__ = 'flatmate'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(40), nullable=True, unique=True) # as connection possibility
    password = db.Column(db.String(250), nullable=True)
    type = db.Column(db.Boolean, nullable=True) # True for providers, False for customers

    preferences = db.relationship('Preferences', backref='flatmate', lazy=True)
    matches = db.relationship('Matches', backref='flatmate', lazy=True)
    offer = db.relationship('Offer', backref='flatmate', lazy=True)

# table for the preferences
class Preferences(db.Model):
    __tablename__ = 'preferences'
    user_id = db.Column(db.Integer, db.ForeignKey('flatmate.id'), primary_key=True)
    pets = db.Column(db.Boolean, nullable=True) # True if animals are no problem
    smoking = db.Column(db.Boolean, nullable=True)
    sex = db.Column(db.Boolean, nullable=True) # True for male, False for female
    age = db.Column(db.Integer, nullable=True)
    relationship_status = db.Column(db.Boolean, nullable=True) # True for committed, False for single
    degree = db.Column(db.Boolean, nullable=True) # True for Master, False for Bachelor
    language = db.Column(db.String(20), nullable=True)
    community = db.Column(db.Integer, nullable=True) # Scale from 1 to 3
    attendance = db.Column(db.Boolean, nullable=True) # True for weekend there, False for weekend away
    semester = db.Column(db.Integer, nullable=True)
    fitness = db.Column(db.Boolean, nullable=True) # True for sportive, No for not sportive

# tables for the matches
class Matches(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    # flatmate matched with offer
    user_id = db.Column(db.Integer, db.ForeignKey('flatmate.id'), nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    # the matching score between the users and between the flatmate and the offer
    score = db.Column(db.Float, nullable=True)
    successful_match = db.Column(db.Integer, nullable=True) # 0 for nothing, 1 for pending, 2 for successful, 3 for rejected

# tables for the flat offers
# for MVP pre configured (+ provider accounts)
class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('flatmate.id'), nullable=False)
    title = db.Column(db.String(40), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    price = db.Column(db.Float, nullable=True)
    distance = db.Column(db.Float, nullable=True)
    apartment_size = db.Column(db.Float, nullable=True)
    room_size = db.Column(db.Float, nullable=True)
    roommates = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)

    matches = db.relationship('Matches', backref='offer', lazy=True)