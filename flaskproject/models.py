from sqlalchemy.orm import backref
from flaskproject import db

class Patient(db.Model):
    __tablename__="patient"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique = False)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120), unique = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String(20), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.Integer, nullable = False)
    image = db.Column(db.String(1000), nullable = False)
    
    def __repr__(self):
        return f"Patient('{self.fullname}', '{self.email}')" 

class Doctor(db.Model):
    __tablename__="doctor"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), unique = False)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120), unique = False)
    image = db.Column(db.String(1000))

    def __repr__(self):
        return f"Doctor('{self.fullname}', '{self.email}')" 