
from flaskproject import app, db
from flask import request, session, url_for, make_response
from flask.json import jsonify
from werkzeug.utils import redirect
import hashlib
from datetime import datetime, timedelta
import jwt
from flaskproject.decorator import token_required
from flaskproject.doctorDecorator import doctoken_required
from flaskproject.models import Patient, Doctor, Prescription
from flask_restful import Api, Resource, reqparse
from flask.templating import render_template


# Home Page route

@app.route('/home')
def home():
    return render_template('homePage.html')

# sign up for patient

@app.route('/signUp')
def signUp():
    return render_template('register.html')

@app.route('/signIn')
def signIn():
    return render_template('login.html')

# Patient Dashboard
@app.route('/patientDashboard')
@token_required
def patientDashboard(current_user):
    patient = Patient.query.filter_by(email = current_user).first()
    return render_template('patientDashboard.html', patient = patient, prescriptions = patient.prescriptions, count = 1)

# Patient Register

@app.route('/createPatient', methods= ["POST", "GET"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest() 

        # register the new patient to the database
        new_user = Patient(fullname = fullname, email = email, password = hashedPassword)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signIn')) #function name and urel_for name should be same
    return {"message": "success"}

# Patient Login

@app.route('/patientLogin', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        hashedPassword = hashedPassword.hexdigest()
        result = Patient.query.filter_by(email = email).first()
        if result == None or hashedPassword != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
        session["jwt"] = token
        return redirect(url_for('patientDashboard'))
    return jsonify({"jwt": "token"}) 
    
# Patient Profile

@app.route('/patientProfile', methods= ["POST", "GET"])
@token_required
def profile(current_user):
    if request.method == "POST":
        patient = Patient.query.filter_by(email = current_user).first()
        patient.age = request.json["age"]
        patient.gender = request.json["gender"]
        patient.address = request.json["address"]
        patient.phone = request.json["phone"]
        db.session.commit()
    return jsonify({"update": "success"})

# Doctor Login

@app.route('/doctorLogin', methods = ["POST", "GET"])
def docLogin():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        # hashedPassword = hashlib.md5(bytes(str(password),encoding='utf-8'))
        # hashedPassword = hashedPassword.hexdigest() 
        result = Doctor.query.filter_by(email = email).first()
        if result == None or password != result.password:
            return "Invalid email or password"
        token = jwt.encode({'user':result.email, 'exp': datetime.utcnow()+timedelta(minutes=15)}, app.config['SECRET_KEY'])
        session["jwt"] = token
        return redirect(url_for('doctorDashboard'))
    return render_template('doctorslogin.html')

# Doctor Profiles

@app.route('/doctorProfiles', methods= ["POST", "GET"])
@doctoken_required
def doctorProfiles(current_user):
    doctors = Doctor.query.all()
    return render_template('doctorProfiles.html',doctors = doctors)

@app.route('/vitalProfiles', methods= ["POST", "GET"])
@token_required
def vitalProfiles(current_user):
    patient = Patient.query.filter_by(email = current_user).first()
    vital = Prescription.query.filter_by(patient_id = patient.id).order_by(Prescription.id.desc()).first()
    return render_template('vitals.html',vital = vital)



@app.route('/prescribe/<patient_id>', methods= ["POST", "GET"])
@doctoken_required
def prescribe(current_user, patient_id):
    if request.method == "POST":
        doctor = Doctor.query.filter_by(email = current_user).first()
        bloodPressure = request.form["bp"]
        heartRate = request.form["hr"]
        glucoseLevel = request.form["gl"]
        bloodCount = request.form["bc"]
        oxygenLevel = request.form["bt"]
        bodyWeight = request.form["bw"]
        diagnosisName = request.form["dname"]
        severity = request.form["severe"]
        medicationitem = request.form["drugName"]
        namedTimeEvent = request.form["timeEvent"]
        doseUnits = request.form["munit"]
        doseVolumne = request.form["dunit"]
        frequency = request.form["frequency"]
        interval = request.form["interval"]
        repetetion = request.form["repetition"]
        additionalInstructions = request.form["description"]
        prescription = Prescription(doctor_id = doctor.id, patient_id = patient_id, bloodPressure = bloodPressure, heartRate = heartRate, glucoseLevel = glucoseLevel, bloodCount = bloodCount, oxygenLevel = oxygenLevel, bodyWeight = bodyWeight, diagnosisName = diagnosisName, severity = severity, medicationitem = medicationitem, namedTimeEvent = namedTimeEvent, doseUnits = doseUnits, doseVolumne = doseVolumne, frequency = frequency, interval = interval, repetetion = repetetion, additionalInstructions = additionalInstructions)
        db.session.add(prescription)
        db.session.commit()
        return redirect(url_for('doctorDashboard'))
    return render_template('prescription.html')

# @app.route('/prescribeForm', methods= ["POST", "GET"])
# @doctoken_required
# def prescribeForm(current_user):
#     return render_template('prescription.html')


# Doctor Dashboard

@app.route('/doctorDashboard', methods= ["POST", "GET"])
@doctoken_required
def doctorDashboard(current_user):
    patients = Patient.query.all()
    return render_template('doctorDashboard.html', patients = patients)


@app.route('/myPatients', methods= ["POST", "GET"])
@doctoken_required
def myPatients(current_user):
    tempList = []
    prescriptions = Prescription.query.all()
    for prescription in prescriptions:
        if prescription.doctor.email == current_user:
            patient = Patient.query.filter_by(id = prescription.patient_id).first()
            tempList.append(patient)
    return render_template('doctorDashboard.html', patients = tempList)
