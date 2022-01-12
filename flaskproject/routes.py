
from flaskproject import app, db
from flask import request, session, url_for, make_response
from flask.json import jsonify
from werkzeug.utils import redirect
import hashlib
from datetime import datetime, timedelta
import jwt
from flaskproject.decorator import token_required
from flaskproject.models import Patient

@app.route('/createPatient', methods= ["POST", "GET"])
def register():
    if request.method == "POST":
        fullname = request.json["fullname"]
        email = request.json["email"]
        password = request.json["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest() 

        # register the new patient to the database
        new_user = Patient(fullname = fullname, email = email, password = hashedPassword)
        db.session.add(new_user)
        db.session.commit()
    return jsonify({"message": "success"})

@app.route('/patientLogin', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.json["email"]
        password = request.json["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        result = Patient.query.filter_by(email = email).first()
        if result == None or hashedPassword != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
        session["jwt"] = token
    return jsonify({"jwt": token}) 
    