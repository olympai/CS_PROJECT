# here we define the tables of our database

from flask_login import UserMixin
from . import db

# table for the users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=True, unique=True)
    password = db.Column(db.String(250), nullable=True)

    preferences = db.relationship('Preferences', backref='user', lazy=True)

# table for the preferences
class Preferences(db.Model):
    __tablename__ = 'preferences'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ...
    # add some parameters

# further tables for matchmaking etc

