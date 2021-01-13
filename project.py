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
    mycursor.execute("CREATE TABLE patients (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientGender ENUM('Female','Male'),PatientBD VARCHAR(50),PatientSSN INT NOT NULL PRIMARY KEY,PatientMaritalStat ENUM('Single','Married','Widowed','Divorced'),PatientHeight VARCHAR(50),PatientWeight VARCHAR(50),PatientBloodGrp VARCHAR(5),PatientPhone VARCHAR(50),PatientEmail VARCHAR(250) NOT NULL UNIQUE,PatientPass VARCHAR(50))")
mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('doctors',):
        y = False
if y:
    mycursor.execute("CREATE TABLE doctors (DoctorFName VARCHAR(50),DoctorMName VARCHAR(50),DoctorLName VARCHAR(50),DoctorAddress VARCHAR(250),DoctorNationality VARCHAR(25),DoctorGender ENUM('Female','Male'),DoctorBD VARCHAR(50),DoctorSSN INT NOT NULL PRIMARY KEY,DoctorMaritalStat ENUM('Single','Married','Widowed','Divorced'),DoctorPhone VARCHAR(50),DoctorBankNum VARCHAR(50),DoctorPass VARCHAR(50),DoctorEmail VARCHAR(250) NOT NULL UNIQUE,DoctorSalary INT,DoctorShift VARCHAR(50),DoctorEmpDate VARCHAR(50))")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/PatientSignIn', methods=["GET", "POST"])
def PatientSignIn():
    if request.method == "POST":
        UserName = request.form['SignInPatientUsername']
        Passwd = request.form['SignInPatientPassword']
        mycursor.execute("SELECT PatientEmail FROM patients")
        emails = mycursor.fetchall()
        for email in emails:
            if email[0] == UserName:
                mycursor.execute(
                    "SELECT PatientPass FROM patients WHERE PatientEmail = '%s'" % (email))
                password = mycursor.fetchone()
                if password[0] == Passwd:
                    data=email[0]
                    return render_template('PatientRecords.html' , email=data)
        else:
                return render_template('PatientSignIn.html')
    else:
        return render_template('PatientSignIn.html')


@app.route('/PatientSignUp', methods=["GET", "POST"])
def PatientSignUp():
    if request.method == "POST":
        Patientfirstname = request.form['PatientFname']
        Patientlastname = request.form['PatientLname']
        Patientgender = request.form['PatientGender']
        Patientbirthdate = request.form['PatientBD']
        Patientssn = request.form['PatientSSN']
        Patientmaritalstat = request.form['PatientMaritalStat']
        Patientheight = request.form['PatientHeight']
        Patientweight = request.form['PatientWeight']
        Patientbloodgrp = request.form['PatientBloodGrp']
        Patientphone = request.form['PatientPhone']
        Patientemail = request.form['PatientEmail']
        Patientpass = request.form['PatientPass']
        sql = "INSERT INTO patients (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (Patientfirstname, Patientlastname, Patientgender, Patientbirthdate, Patientssn, Patientmaritalstat,
               Patientheight, Patientweight, Patientbloodgrp, Patientphone, Patientemail, Patientpass)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('index.html')
    else:
        return render_template('PatientSignUp.html')

'''
@app.rout('/PatientPanel/##')##
def PatientViewProfile():
    mycursor.execute("SELECT *FROM patients WHERE PatientEmail  = '%s'" % (email))
    data = mycursor.fetchall()
    return render_template('PatientRecords.html', patientsdata=data)#eb3ty el data hnak fy el html


@app.route('/PatientPanel/##') ##
def PatientUpdateProfile():
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
'''


@app.route('/PatientPanel/PatientAddAppoint', methods=['POST','GET']) ##
def PatientViewAppoint():
    if request.method == 'GET':
        mycursor.execute("SELECT DoctorFName DoctorMName DoctorLName DoctorShift FROM doctors")
        data = mycursor.fetchall()
        return render_template("PatientAddAppoint.html", appoint=data)



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


@app.route('/AdminPanel/AddDoctor', methods=['POST', 'GET'])
def AddDoctor():
    if request.method == 'POST':
        Fname = request.form['DoctorFName']
        Mname = request.form['DoctorMName']
        Lname = request.form['DoctorLName']
        Address = request.form['DoctorAddress']
        Nationality = request.form['DoctorNationality']
        Gender = request.form['DoctorGender']
        BD = request.form['DoctorBD']
        SSN = request.form['DoctorSSN']
        MaritalStat = request.form['DoctorMaritalStat']
        Phone = request.form['DoctorPhone']
        BankNum = request.form['DoctorBankNum']
        Pass = request.form['DoctorPass']
        Email = request.form['DoctorEmail']
        DoctorSalary = request.form['DoctorSalary']
        DoctorShift = request.form['DoctorShift']
        DoctorEmpDate = request.form['DoctorEmploymentDate']
        sql = "INSERT INTO doctors (DoctorFName,DoctorMName,DoctorLName,DoctorAddress,DoctorNationality,DoctorGender,DoctorBD,DoctorSSN,DoctorMaritalStat,DoctorPhone,DoctorBankNum,DoctorPass,DoctorEmail,DoctorSalary,DoctorShift,DoctorEmpDate) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (Fname, Mname, Lname, Address, Nationality, Gender,
               BD, SSN, MaritalStat, Phone, BankNum, Pass, Email,DoctorSalary,DoctorShift,DoctorEmpDate)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('AdminPanel.html')
    else:
        return render_template('AddDoctor.html')


@app.route('/AdminPanel/DoctorRecords')
def DoctorRecords():
    mycursor.execute("SELECT * FROM doctors")
    data = mycursor.fetchall()
    return render_template('DoctorRecords.html', doctorsdata=data)


@app.route('/AdminPanel/PatientRecords')
def PatientRecords():
    mycursor.execute("SELECT * FROM patients")
    data = mycursor.fetchall()

    return render_template('PatientRecords.html', patientsdata=data)


app.run(port=5000, debug=True)
