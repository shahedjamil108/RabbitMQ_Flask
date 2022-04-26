from . import db
from flask_login import UserMixin

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    roll = db.Column(db.String(30))
    feedback = db.Column(db.String(30))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    result = db.Column(db.String(30))
    roll = db.Column(db.String(30))
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    roll = db.Column(db.String(150), unique = True)
    section = db.Column(db.String(30))    
    password = db.Column(db.String(30))
    #result = db.relationship('Result')    
