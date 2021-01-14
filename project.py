import os
from flask import Flask, request, render_template, url_for, redirect, session, flash
#from werkzeug import secure_filename
#from flask_login import LoginManager
import mysql.connector

#login_manager = LoginManager()

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
    mycursor.execute("CREATE TABLE patients (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientGender ENUM('Female','Male'),PatientBD VARCHAR(50),PatientSSN INT NOT NULL PRIMARY KEY,PatientMaritalStat ENUM('Single','Married','Widowed','Divorced'),PatientHeight VARCHAR(50),PatientWeight VARCHAR(50),PatientBloodGrp VARCHAR(5),PatientPhone VARCHAR(50),PatientEmail VARCHAR(250) NOT NULL UNIQUE,PatientPass VARCHAR(50),ConfirmPatientPass VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('doctors',):
        y = False
if y:
    mycursor.execute("CREATE TABLE doctors (DoctorFName VARCHAR(50),DoctorMName VARCHAR(50),DoctorLName VARCHAR(50),DoctorAddress VARCHAR(250),DoctorNationality VARCHAR(25),DoctorGender ENUM('Female','Male'),DoctorBD VARCHAR(50),DoctorSSN INT NOT NULL PRIMARY KEY,DoctorMaritalStat ENUM('Single','Married','Widowed','Divorced'),DoctorPhone VARCHAR(50),DoctorBankNum VARCHAR(50),DoctorEmail VARCHAR(250) NOT NULL UNIQUE,DoctorPass VARCHAR(50),DoctorSalary INT,DoctorShift VARCHAR(50),DoctorEmpDate VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('appointments',):
        y = False
if y:
    mycursor.execute("CREATE TABLE appointments (PatientFname VARCHAR(50),AppointmentDate VARCHAR(50),AppointmentTime VARCHAR(50),Doctorname VARCHAR(50),PatientEmail VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('devices',):
        y = False
if y:
    mycursor.execute("CREATE TABLE devices (DeviceSerialNo INT NOT NULL PRIMARY KEY,DeviceBrand VARCHAR(50),TotalDialysis VARCHAR(50),LastMaint VARCHAR(50),NextMaint VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('testresults',):
        y = False
if y:
    mycursor.execute("CREATE TABLE testresults (TestName VARCHAR(50),TestDate VARCHAR(50),TestFile VARCHAR(333))")

app = Flask(__name__)
app.secret_key = 'mew'

#login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/PatientSignIn', methods=["GET", "POST"])
def PatientSignIn():
    if request.method == "POST":
        PatientUserName = request.form['SignInPatientUsername']
        PatientPasswd = request.form['SignInPatientPassword']
        mycursor.execute("SELECT * FROM patients WHERE PatientEmail = %s AND PatientPass = %s ",
                         (PatientUserName, PatientPasswd))
        email = mycursor.fetchone()
        if email:
            session['loggedin'] = True
            session['id'] = PatientUserName
            session['username'] = PatientUserName
            return render_template('PatientPanel.html')
        else:
            return render_template('PatientSignIn.html', er='Incorretct Email or Password')
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
        ConfirmPatientPass = request.form['ConfirmPatientPass']
        if Patientpass != ConfirmPatientPass:
            return render_template('PatientSignUp.html',msg="Password doesn't match")
        sql = "INSERT INTO patients (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (Patientfirstname, Patientlastname, Patientgender, Patientbirthdate, Patientssn, Patientmaritalstat,
               Patientheight, Patientweight, Patientbloodgrp, Patientphone, Patientemail, Patientpass)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('PatientSignUp.html', msg='YOU SIGNED UP SUCCESSFULLY')
    else:
        return render_template('PatientSignUp.html')


@app.route('/PatientPanel/ViewPatientProfile')
def PatientViewProfile():
    mycursor.execute(
        "SELECT * FROM  patients WHERE PatientEmail = %s ", (session['username'],))
    email = mycursor.fetchone()
    return render_template('ViewPatientProfile.html', data=email)


@app.route('/PatientPanel/UpdatePatientProfile')
def UpdatePatientProfile():
    if request.method == 'POST':
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
        sql = "UPDATE patients SET PatientFname=%s,PatientLname=%s,PatientGender=%s,PatientBD=%s,PatientSSN=%s,PatientMaritalStat=%s,PatientHeight=%s,PatientWeight=%s,PatientBloodGrp=%s,PatientPhone=%s,PatientEmail=%s,PatientPass=%s PatientEmail=%s WHERE PatientEmail=%s"
        val = (Patientfirstname, Patientlastname, Patientgender, Patientbirthdate, Patientssn, Patientmaritalstat,
               Patientheight, Patientweight, Patientbloodgrp, Patientphone, Patientemail, Patientpass,session['username'])
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('ViewPatientProfile.html',msg='YOU UPDATED YOUR PROFILE SUCCESSFULLY')
    else:
        return render_template('UpdatePatientProfile.html')


@app.route('/PatientPanel/PatientAddAppoint')
def PatientViewAppoints():
    mycursor.execute("SELECT DoctorFName, DoctorMName, DoctorShift FROM doctors")
    data = mycursor.fetchall()
    return render_template("PatientAddAppoint.html", appoint=data)


@app.route('/PatientPanel/PatientAddAppoint', methods=['POST', 'GET'])
def PatientAddAppoint():
    if request.method == 'POST':
        AppointmentDate = request.form['PatientApointDay']
        AppointmentTime = request.form['PatientApointTime']
        Doctorname = request.form['PatientApointDoc']
        mycursor.execute(
        "SELECT PatientFname PatientLname FROM  patients WHERE PatientEmail = %s ", (session['username'],))
        Patient_name = mycursor.fetchone()
        sql = "INSERT INTO appointments (PatientFname,AppointmentDate,AppointmentTime,Doctorname,PatientEmail) VALUES (%s,%s,%s,%s,%s)"
        val = (Patient_name[0],AppointmentDate, AppointmentTime, Doctorname,session['username'])
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('PatientViewAppoints.html')
    else:
        return render_template('PatientAddAppoint.html')


@app.route('/PatientPanel/PatientViewAppoint')
def PatientViewMyAppoint():
    mycursor.execute(
        "SELECT AppointmentDate AppointmentTime Doctorname FROM appointments WHERE PatientEmail = %s ", (session['username'],))
    data = mycursor.fetchall()
    return render_template('PatientViewAppoints.html', app=data)


@app.route('/PatientPanel/PatientTestResults',methods=['POST','GET'])
def PatientTestResults():
    if request.method == 'POST':
        TestName = request.form['TestName']
        TestDate = request.form['TestDate']
        #TestFile = request.form['TestFile']
        #TestFile = request.files['TestFile']
        #TestFile.save(secure_filename(TestFile.filename))
        sql = "INSERT INTO testresults (TestName,TestDate) VALUES (%s,%s)"
        val = (TestName,TestDate)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('PatientTestResults.html')
    else:
        return render_template('PatientTestResults.html')


@app.route('/PatientPanel/PatientTestResults')
def ViewTestResults():
    mycursor.execute("SELECT *FROM testresults")
    data = mycursor.fetchall()
    return render_template('PatientTestResults.html',TestData=data)


@app.route('/DoctorSignIn', methods=["GET", "POST"])
def DoctorSignIn():
    if request.method == "POST":
        DoctorUserName = request.form['SignInDoctorUsername']
        DoctorPasswd = request.form['SignInDoctorPassword']
        mycursor.execute(
            "SELECT * FROM doctors WHERE DoctorEmail = %s AND DoctorPass = %s ", (DoctorUserName, DoctorPasswd))
        DoctorInfo = mycursor.fetchone()
        if DoctorInfo:
            session['loggedin'] = True
            session['id'] = DoctorUserName
            session['username'] = DoctorUserName
            return render_template('DoctorPanel.html')
        else:
            return render_template('DoctorSignIn.html', er='Incorretct Email or Password')
    else:
        return render_template('DoctorSignIn.html')


@app.route('/AdminSignIn', methods=['GET', 'POST'])
def AdminSignIn():
    if request.method == 'POST':
        UserName = request.form['SignInAdminUsername']
        Pass = request.form['SignInAdminPassword']
        if UserName == 'Admin@hos' and Pass == '1234':
            #return AdminPanel()
            return redirect(url_for('AdminPanel'))
        else:
            return render_template('AdminSignIn.html', error='Incorrect Email or Password')
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
               BD, SSN, MaritalStat, Phone, BankNum, Pass, Email, DoctorSalary, DoctorShift, DoctorEmpDate)
        mycursor.execute(sql, val)
        mydb.commit()
        return AdminPanel()
    else:
        return render_template('AddDoctor.html')


@app.route('/AdminPanel/AddDevice', methods=['POST', 'GET'])
def AddDevice():
    if request.method == 'POST':
        SerialNumber = request.form['DeviceSerialNo']
        Brand = request.form['DeviceBrand']
        DialysisPerDay = request.form['TotalDialysis']
        LastMent = request.form['LastMaint']
        UpcomingMent = request.form['NextMaint']
        sql = "INSERT INTO devices (DeviceSerialNo,DeviceBrand,TotalDialysis,LastMaint,NextMaint) VALUES(%s,%s,%s,%s,%s)"
        val = (SerialNumber, Brand, DialysisPerDay, LastMent, UpcomingMent)
        mycursor.execute(sql, val)
        mydb.commit()
       # return AdminPanel()
        return redirect(url_for('AdminPanel'))
    else:
        return render_template('AddDevice.html')


@app.route('/AdminPanel/AdminUpdate', methods=['POST', 'GET'])
def AdminUpdate():
    if request.method == 'POST':
        pass

    return render_template('AdminUpdate.html')


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


@app.route('/SignOut')
def logout():
   session.clear()
   return render_template('index.html')


app.run(port=5000, debug=True)
