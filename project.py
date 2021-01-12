from flask import Flask, jsonify, request, render_template

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql"
)

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
y = True
for x in mycursor:
    if x == ('hosmansys',):
        y = False
if y:
    mycursor.execute("CREATE DATABASE hosmansys")


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="hosmansys"
)
mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('patients',):
        y = False
if y:
    mycursor.execute("CREATE TABLE patients (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientGender VARCHAR(50),PatientBD VARCHAR(50),PatientSSN VARCHAR(50),PatientMaritalStat VARCHAR(50),PatientHeight VARCHAR(50),PatientWeight VARCHAR(50),PatientBloodGrp VARCHAR(50),PatientPhone VARCHAR(50),PatientEmail VARCHAR(50),PatientPass VARCHAR(50))")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/PatientSignIn')
def PatientSignIn():
    return render_template('PatientSignIn.html')


@app.route('/PatientSignUp', methods=["GET", "POST"])
def PatientSignUp():
    if request.method == "POST":
        PatientFname = request.form['PatientFname']
        PatientLname = request.form['PatientLname']
        PatientGender = request.form['PatientGender']
        PatientBD = request.form['PatientBD']
        PatientSSN = request.form['PatientSSN']
        PatientMaritalStat = request.form['PatientMaritalStat']
        PatientHeight = request.form['PatientHeight']
        PatientWeight = request.form['PatientHeight']
        PatientBloodGrp = request.form['PatientBloodGrp']
        PatientPhone = request.form['PatientPhone']
        PatientEmail = request.form['PatientEmail']
        PatientPass = request.form['PatientPass']
        sql = "INSERT INTO patients (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (PatientFname, PatientLname, PatientGender, PatientBD, PatientSSN, PatientMaritalStat,
               PatientHeight, PatientWeight, PatientBloodGrp, PatientPhone, PatientEmail, PatientPass)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('index.html')
    else:
        return render_template('PatientSignUp.html')


@app.route('/DoctorSignIn')
def DoctorSignIn():
    return render_template('DoctorSignIn.html')


@app.route('/AdminSignIn', methods=["GET", "POST"])
def AdminSignIn():

    if request.method == "POST":

        return render_template('AdminPanel.html')
    else:
        return render_template('AdminSignIn.html')


@app.route('/AdminPanel')
def AdminPanel():
    return render_template('AdminPanel.html')


@app.route('/AdminPanel/DoctorRecords')
def DoctorRecords():
    mycursor.execute("SELECT * FROM Patients")
    data = mycursor.fetchall()

    return render_template('PatientRecords.html', doctorsdata=data)


app.run(port=5000, debug=True)
