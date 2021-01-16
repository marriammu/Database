from flask import Flask, request, render_template, url_for, redirect, session, send_from_directory

# from flask_uploads import UploadSet, configure_uploads, IMAGES
#from werkzeug.utils import secure_filename
#from werkzeug.datastructures import FileStorage

import os
import secrets
import mysql.connector
import datetime
import pickle
import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request


app = Flask(__name__)
app.secret_key = 'mew'

# photos = UploadSet('photos',IMAGES)
# app.config['UPLOADED_PHOTOS_DEST']='static'
# configure_uploads(app,photos)


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
    mycursor.execute("CREATE TABLE patients (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientGender ENUM('Female','Male'),PatientBD VARCHAR(50),PatientSSN VARCHAR(50),PatientMaritalStat ENUM('Single','Married','Widowed','Divorced'),PatientHeight VARCHAR(50),PatientWeight VARCHAR(50),PatientBloodGrp VARCHAR(5),PatientPhone VARCHAR(50),PatientEmail VARCHAR(250) NOT NULL UNIQUE,PatientPass VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('doctors',):
        y = False
if y:
    mycursor.execute("CREATE TABLE doctors (DoctorFName VARCHAR(50),DoctorMName VARCHAR(50),DoctorLName VARCHAR(50),DoctorAddress VARCHAR(250),DoctorNationality VARCHAR(25),DoctorGender ENUM('Female','Male'),DoctorBD VARCHAR(50),DoctorSSN INT ,DoctorMaritalStat ENUM('Single','Married','Widowed','Divorced'),DoctorPhone VARCHAR(50),DoctorBankNum VARCHAR(50),DoctorEmploymentDate DATE,DoctorSalary INT,DoctorShift ENUM('12 PM','4 PM','8 PM','12 AM','4 AM','8 AM'),DoctorEmail VARCHAR(250),DoctorPass VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('appointments',):
        y = False
if y:
    mycursor.execute("CREATE TABLE appointments (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientEmail VARCHAR(50),AppointmentDate VARCHAR(50),AppointmentTime VARCHAR(50),DoctorFName VARCHAR(50),DoctorMName VARCHAR(50),DoctorLName VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('devices',):
        y = False
if y:
    mycursor.execute("CREATE TABLE devices (DeviceSerialNo INT,DeviceBrand VARCHAR(50),TotalDialysis VARCHAR(50),LastMaint VARCHAR(50),NextMaint VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('feedback',):
        y = False
if y:
    mycursor.execute("CREATE TABLE feedback (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientEmail VARCHAR(50),PatientContactUs VARCHAR(3000))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('testresults',):
        y = False
if y:
    mycursor.execute(
        "CREATE TABLE testresults (PatientFname VARCHAR(50),PatientLname VARCHAR(50),TestName VARCHAR(50),TestDate VARCHAR(50),TestFile VARCHAR(333))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('medicalhistory',):
        y = False
if y:
    mycursor.execute("CREATE TABLE medicalhistory (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientEmail VARCHAR(50),ChronicDisease VARCHAR(500),Prescription VARCHAR(500),EmergencyMed VARCHAR(500),Alergies VARCHAR(500),SurgicalHistory VARCHAR(500),Fracture VARCHAR(500),Smoker VARCHAR(500))")


@app.route('/')
def index():
    return render_template('index.html')


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
        mycursor.execute("SELECT PatientEmail FROM patients")
        patientE = mycursor.fetchall()
        for x in patientE:   
            if x[0] == Patientemail:
                return render_template('PatientSignUp.html', msg='Email already exists')
            else:
                continue
        mycursor.execute("SELECT PatientSSN FROM patients")
        patientS = mycursor.fetchall()
        for x in patientS:               
            if x[0] == Patientssn:
                return render_template('PatientSignUp.html', msg='SSN already exists')
            else:
                continue
        if Patientpass != ConfirmPatientPass:
            return render_template('PatientSignUp.html', msg="Password doesn't match")
        else:
            sql = "INSERT INTO patients (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (Patientfirstname, Patientlastname, Patientgender, Patientbirthdate, Patientssn, Patientmaritalstat,
                   Patientheight, Patientweight, Patientbloodgrp, Patientphone, Patientemail, Patientpass)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('PatientSignUp.html', msg='YOU SIGNED UP SUCCESSFULLY')
    else:
        return render_template('PatientSignUp.html')


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
            session['type'] = "patient"
            return render_template('PatientPanel.html')
        else:
            return render_template('PatientSignIn.html', er='Incorretct Email or Password')
    else:
        return render_template('PatientSignIn.html')


@app.route('/PatientPanel/ViewPatientProfile')
def PatientViewProfile():
    if session['type'] == 'patient':
        mycursor.execute(
            "SELECT * FROM  patients WHERE PatientEmail = %s ", (session['username'],))
        email = mycursor.fetchone()
        return render_template('ViewPatientProfile.html', data=email)
    else:
        return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


@app.route('/PatientPanel/UpdatePatientProfile', methods=['POST', 'GET'])
def UpdatePatientProfile():
    if session['type'] == 'patient':
        if request.method == 'POST':
            PatientFname = request.form['PatientFname']
            PatientLname = request.form['PatientLname']
            PatientGender = request.form['PatientGender']
            PatientBD = request.form['PatientBD']
            PatientSSN = request.form['PatientSSN']
            PatientMaritalStat = request.form['PatientMaritalStat']
            PatientHeight = request.form['PatientHeight']
            PatientWeight = request.form['PatientWeight']
            PatientBloodGrp = request.form['PatientBloodGrp']
            PatientPhone = request.form['PatientPhone']
            PatientEmail = request.form['PatientEmail']
            PatientPass = request.form['PatientPass']
            mycursor.execute("SELECT *FROM  patients WHERE PatientEmail = %s ", (session['username'],))
            patientdata = mycursor.fetchone()
            sql = "UPDATE patients SET PatientFname=%s,PatientLname=%s,PatientGender=%s,PatientBD=%s,PatientSSN=%s,PatientMaritalStat=%s,PatientHeight=%s,PatientWeight=%s,PatientBloodGrp=%s,PatientPhone=%s,PatientEmail=%s,PatientPass=%s WHERE PatientEmail =%s"
            val = (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass,session['username'])
            mycursor.execute(sql,val)
            mydb.commit()
            return render_template('UpdatePatientProfile.html', data=patientdata, msg='YOU UPDATED YOUR PROFILE SUCCESSFULLY')
        else:
            mycursor.execute("SELECT *FROM  patients WHERE PatientEmail = %s ", (session['username'],))
            patientdata = mycursor.fetchone()
            return render_template('UpdatePatientProfile.html', data=patientdata)
    else:
            return render_template('PatientSignIn.html', er='PLEASE SIGN IN')

@app.route('/PatientPanel/PatientViewShifts')
def PatientViewShifts():
    if session['type']=='patient':
        mycursor.execute("SELECT DoctorFName, DoctorMName, DoctorShift FROM doctors")
        data = mycursor.fetchall()
        return render_template("PatientViewShifts.html", appoint=data)
    else:
        return render_template('PatientSignIn.html', er='PLEASE SIGN IN')

@app.route('/PatientPanel/PatientAddAppoint', methods=['POST', 'GET'])
def PatientAddAppoint():
    if session['type'] == 'patient':
        if request.method == 'POST':
            PatientApointDay = request.form['PatientApointDay']
            PatientApointTime = request.form['PatientApointTime']
            PatientApointDocF = request.form['PatientApointDocF']
            PatientApointDocM = request.form['PatientApointDocM']
            PatientApointDocL = request.form['PatientApointDocL']
            mycursor.execute("SELECT PatientFname FROM patients WHERE PatientEmail = %s ", (session['username'],))
            PatientFname = mycursor.fetchone()
            mycursor.execute("SELECT PatientLname FROM patients WHERE PatientEmail = %s ", (session['username'],))
            PatientLname = mycursor.fetchone()
            sql = "INSERT INTO appointments (PatientFname,PatientLname,AppointmentDate,AppointmentTime,DoctorFName,DoctorMName,DoctorLName,PatientEmail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (PatientFname[0],PatientLname[0],PatientApointDay, PatientApointTime, PatientApointDocF,PatientApointDocM,PatientApointDocL,session['username'])
            mycursor.execute(sql, val)
            mydb.commit()
            #Calendar(PatientApointDay,PatientApointTime)
            return render_template('PatientAddAppoint.html')
        else:
            return render_template('PatientAddAppoint.html')
    else:
        return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


@app.route('/PatientPanel/PatientViewAppoints')
def PatientViewMyAppoint():
    if session['type'] == 'patient':
        mycursor.execute("SELECT AppointmentDate,AppointmentTime,DoctorFName,DoctorMName,DoctorLName FROM appointments")
        data = mycursor.fetchall()
        return render_template("PatientViewAppoints.html", app=data)   
    else:
        return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


# @app.route('/PatientPanel/PatientAddTestResults',methods = ['GET','POST'])
# def PatientAddTestResults():
#     if session['type'] == 'patient':
#         if request.method == 'POST' and 'photo' in request.files:
#             # print('ay 7aga')
#             # data = request.files
#             # print('wala 7aga')
#             # print(data)
#             filename = photos.save(request.files['photo'])
#             #return filename
#             session['photo'] = filename
#             return render_template("PatientViewTestResults.html", image_name=filename)
#            # return send_from_directory('static/img',filename ,as_attachment=True)
#         else:
#             return render_template('PatientAddTestResults.html')
#     else:    
#         return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


# @app.route('/PatientPanel/PatientViewTestResults')
# def PatientViewTestResults():
#     if session['type']=='patient':
#         # mycursor.execute("SELECT *FROM testresults")
#         # data = mycursor.fetchall()
#         return render_template("PatientViewTestResults.html",image_name=session['photo'])
#     else:
#         return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


@app.route('/PatientPanel/PatientContactUs', methods=['POST', 'GET'])
def PatientContactUs():
    if session['type'] == 'patient':
        if request.method == 'POST':
            PatientContactUs = request.form['PatientContactUs']
            mycursor.execute("SELECT PatientFname FROM patients WHERE PatientEmail = %s ", (session['username'],))
            data1 = mycursor.fetchone()
            mycursor.execute("SELECT PatientLname FROM patients WHERE PatientEmail = %s ", (session['username'],))
            data2 = mycursor.fetchone()
            sql = "INSERT INTO feedback (PatientFname,PatientLname,PatientEmail,PatientContactUs) VALUES (%s,%s,%s,%s)"
            val = (data1[0],data2[0],session['username'],PatientContactUs)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('/PatientContactUs.html')
        else:
            return render_template('/PatientContactUs.html')  
    else:        
        return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


@app.route('/PatientPanel/PatientMedicalHistory',methods=['POST','GET']) #zoraar el submit msh sha8al
def PatientMedicalHistory():
    if session['type'] == 'patient':
        if request.method == 'POST':
            ChronicDisease = request.form['ChronicDisease']
            Prescription = request.form['ChronicDisease']
            EmergencyMed = request.form['EmergencyMed']
            Alergies = request.form['Alergies']
            SurgicalHistory = request.form['SurgicalHistory']
            Fracture= request.form['Fracture']
            Smoker = request.form['Smoker']
            mycursor.execute("SELECT PatientFname FROM patients WHERE PatientEmail = %s ", (session['username'],))
            data1 = mycursor.fetchone()
            mycursor.execute("SELECT PatientLname FROM patients WHERE PatientEmail = %s ", (session['username'],))
            data2 = mycursor.fetchone()  
            sql = "INSERT INTO medicalhistory (PatientFname,PatientLname,PatientEmail,ChronicDisease,Prescription,EmergencyMed,Alergies,SurgicalHistory,Fracture,Smoker) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (data1[0],data2[0],session['username'],ChronicDisease,Prescription,EmergencyMed,Alergies,SurgicalHistory,Fracture,Smoker)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('/PatientMedicalHistory.html')
        else:
            return render_template('/PatientMedicalHistory.html')
    else:
        return render_template('PatientSignIn.html', er='PLEASE SIGN IN')


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
            session['type']='doctor'
            return render_template('DoctorPanel.html')
        else:
            return render_template('DoctorSignIn.html', er='Incorretct Email or Password')
    else:
        return render_template('DoctorSignIn.html')


@app.route('/DoctorPanel/ViewDoctorProfile')
def ViewDoctorProfile():
    if session['type'] == 'doctor':    
        mycursor.execute("SELECT* FROM doctors WHERE DoctorEmail= %s ",(session['username'],) )
        myresult=mycursor.fetchone()
        return render_template('ViewDoctorProfile.html',data=myresult)
    else:
        return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


@app.route('/DoctorPanel/UpdateDoctorProfile', methods=['POST','GET'])
def UpdateDoctorProfile():
    if session['type'] == 'doctor':
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
            DoctorEmpDate = request.form['DoctorEmploymentDate']
            DoctorSalary = request.form['DoctorSalary']
            DoctorShift = request.form['DoctorShift']
            Email = request.form['DoctorEmail']
            Pass = request.form['DoctorPass']
            mycursor.execute("SELECT* FROM doctors WHERE DoctorEmail=%s",(session['username'],))
            doctorData=mycursor.fetchone()
            sql = "UPDATE doctors SET DoctorFName=%s,DoctorMName=%s ,DoctorLName=%s ,DoctorAddress=%s,DoctorNationality=%s,DoctorGender=%s,DoctorBD=%s,DoctorSSN=%s,DoctorMaritalStat=%s,DoctorPhone=%s,DoctorBankNum=%s,DoctorEmploymentDate=%s,DoctorSalary=%s,DoctorShift=%s,DoctorEmail=%s,DoctorPass=%s WHERE DoctorEmail=%s"
            val = (Fname, Mname, Lname, Address, Nationality, Gender,BD, SSN, MaritalStat, Phone, BankNum, DoctorEmpDate, DoctorSalary, DoctorShift, Email,Pass,session['username'])
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.execute("SELECT* FROM doctors WHERE DoctorEmail=%s",(session['username'],))
            doctorData=mycursor.fetchone()
            return render_template('UpdateDoctorProfile.html',data=doctorData)
        else:
            mycursor.execute("SELECT* FROM doctors WHERE DoctorEmail=%s",(session['username'],))
            doctorData=mycursor.fetchone()
            return render_template('UpdateDoctorProfile.html',data=doctorData)
    else:
        return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


@app.route('/DoctorPanel/DoctorsMedicalHistory')
def medicalhistory():
    if session['type'] == 'doctor':
        mycursor.execute("SELECT* FROM medicalhistory")
        data = mycursor.fetchall()
        return render_template('DoctorsMedicalHistory.html',his=data)
    else:
        return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


@app.route('/DoctorPanel/DoctorsPatientRecords')
def Patient_Records():
    if session['type'] == 'doctor':
        mycursor.execute("SELECT* FROM patients")
        data=mycursor.fetchall()
        return render_template('DoctorsPatientRecords.html',patientsdata=data)
    else:
        return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


@app.route('/DoctorPanel/DoctorsDeviceRecords')
def DoctorsDeviceRecords():
    if session['type'] == 'doctor':
        mycursor.execute("SELECT* FROM devices")
        data=mycursor.fetchall()
        return render_template('DoctorsDeviceRecords.html',DeviceRecords=data)
    else:
        return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


# @app.route('/DoctorPanel/DoctorsTestResults')
# def TestResults():
#     if session['type'] == 'doctor':
#         mycursor.execute("SELECT* FROM testresults")
#         data=mycursor.fetchall()
#         return render_template('DoctorsTestResults.html',TestResults=data)
#     else:
#         return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


@app.route('/DoctorPanel/DoctorViewAppoints')
def DoctorAppoints():
    if session['type'] == 'doctor':    
        mycursor.execute("SELECT DoctorFName,DoctorMName FROM doctors WHERE DoctorEmail=%s",(session['username'],))
        doc = mycursor.fetchone()
        doc1=doc[0]
        doc2=doc[1]
        print(doc1,doc2)
        mycursor.execute("SELECT PatientFname,PatientLname ,AppointmentDate,AppointmentTime FROM appointments WHERE DoctorFName='%s' AND DoctorMName='%s' " %(doc1,doc2))
        data = mycursor.fetchall()
        return render_template('DoctorViewAppoints.html', myresult=data)
    else:
        return render_template('DoctorSignIn.html',er='PLEASE SIGN IN')


@app.route('/AdminSignIn', methods=['GET', 'POST'])
def AdminSignIn():
    if request.method == 'POST':
        UserName = request.form['SignInAdminUsername']
        Pass = request.form['SignInAdminPassword']
        if UserName == 'Admin@hos' and Pass == '1234':
            session['loggedin'] = True
            session['id'] = UserName
            session['username'] = UserName
            session['type']='admin'
            return render_template('AdminPanel.html')
        else:
            return render_template('AdminSignIn.html', error='Incorrect Email or Password')
    else:
        return render_template('AdminSignIn.html')


@app.route('/AdminPanel')
def AdminPanel():
    if session['type'] == 'admin':
        return render_template('AdminPanel.html')
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')    


@app.route('/AdminPanel/AddDoctor', methods=['POST', 'GET'])
def AddDoctor():
    # types = session['type'] 
    # print(types)
    # if session['type'] and 'loggedin' in session:
    if session['type'] == 'admin':
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
            mycursor.execute("SELECT DoctorEmail FROM doctors")
            DoctorE = mycursor.fetchall()
            for x in DoctorE:
                if x[0] == Email:
                    return render_template('AddDoctor.html', msg='Email already exists')
                else:
                    continue
            mycursor.execute("SELECT DoctorSSN FROM doctors")
            doctorS = mycursor.fetchall()
            for x in doctorS:               
                if x[0] == SSN:
                    return render_template('AddDoctor.html', msg='SSN already exists')
                else:
                    continue
            sql = "INSERT INTO doctors (DoctorFName,DoctorMName,DoctorLName,DoctorAddress,DoctorNationality,DoctorGender,DoctorBD,DoctorSSN,DoctorMaritalStat,DoctorPhone,DoctorBankNum,DoctorEmploymentDate,DoctorSalary,DoctorShift,DoctorEmail,DoctorPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (Fname, Mname, Lname, Address, Nationality, Gender,
                BD, SSN, MaritalStat, Phone, BankNum, DoctorEmpDate,  DoctorSalary, DoctorShift, Email, Pass)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('AddDoctor.html', msg='DOCTOR ADDED SUCCESSFULLY')
        else:
            return render_template('AddDoctor.html')
    else:
        print ('wala 7aga')
        print ('type' in session)
        print('loggedin' in session)
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN') 


@app.route('/AdminPanel/DeviceRecords')
def DeviceRecords():
    mycursor.execute("SELECT * FROM devices")
    data = mycursor.fetchall()
    return render_template('DeviceRecords.html', devicesdata=data)


@app.route('/AdminPanel/AddDevice', methods=['POST', 'GET'])
def AddDevice():
    if session['type'] == 'admin':
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
            return redirect(url_for('AdminPanel'))
        else:
            return render_template('AddDevice.html')
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')


@app.route('/AdminPanel/AdminUpdate', methods=['POST', 'GET']) #update device acoording where ssn known
def AdminUpdate():
    if session['type'] == 'admin':
        if request.method == 'POST':
            DeviceSerialNo = request.form['DeviceSerialNo']
            TotalDialysis = request.form['TotalDialysis']
            LastMaint = request.form['LastMaint']
            NextMaint = request.form['NextMaint']
            # mycursor.execute("SELECT DeviceSerialNo FROM devices")
            # devices = mycursor.fetchall()
            # print(devices)
            # print(DeviceSerialNo)
            # for x in devices:
            #     print(x[0])
            #     if x[0] == DeviceSerialNo:
            sql = "UPDATE devices SET TotalDialysis=%s,LastMaint=%s,NextMaint=%s WHERE DeviceSerialNo=%s"
            val = (TotalDialysis, LastMaint, NextMaint,DeviceSerialNo)
            mycursor.execute(sql, val)
            mydb.commit()
            return render_template('AdminUpdate.html',msg='THE DEVICE IS UPDATED')
                # else:
                #     continue
        return render_template('AdminUpdate.html')#,msg='The device is not found') #3ayzeeen msg='ENTER THE S.N OF THE DEVICE lama yd5ol 3shan bnpick ely han2bdetoh 3la asasha'
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')    


@app.route('/AdminPanel/DoctorRecords')
def DoctorRecords():
    if session['type'] == 'admin':
        mycursor.execute("SELECT * FROM doctors")
        data = mycursor.fetchall()
        return render_template('DoctorRecords.html', doctorsdata=data)
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')


@app.route('/AdminPanel/PatientRecords')
def PatientRecords():
    if session['type'] == 'admin':
        mycursor.execute("SELECT * FROM patients")
        data = mycursor.fetchall()
        return render_template('PatientRecords.html', patientsdata=data)
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')


@app.route('/AdminPanel/StatisticalAnalysis')
def StatisticalAnalysis():
    if session['type'] == 'admin':
        mycursor.execute("SELECT DoctorSSN FROM doctors")
        DoctorSSNs = mycursor.fetchall()
        DoctorsNum = len(DoctorSSNs)
        mycursor.execute("SELECT PatientSSN FROM patients")
        PatientSSN = mycursor.fetchall()
        PatientsNum = len(PatientSSN)
        mycursor.execute("SELECT DeviceSerialNo FROM devices")
        DeviceSerialNum = mycursor.fetchall()
        DevicesNumber = len(DeviceSerialNum)
        mycursor.execute("SELECT AppointmentTime FROM appointments")
        Appointment = mycursor.fetchall()
        Appointments = len(Appointment)
        # labels = ['Doctors', 'Patients', 'Devices', 'Appointments']
        # values = [DoctorsNum, PatientsNum, DevicesNumber, Appointments]
        return render_template('StatisticalAnalysis.html',a=DoctorsNum,b=PatientsNum,c=DevicesNumber,d=Appointments)
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')


@app.route('/AdminPanel/AdminAppointments')
def AddAppointments():
    if session['type'] == 'admin':
        mycursor.execute("SELECT *FROM appointments")
        data = mycursor.fetchall()
        return render_template('AdminAppointments.html',app=data)
    else:
        return render_template('AdminSignIn.html',er='PLEASE SIGN IN')


@app.route('/SignOut')
def logout():
    session.clear()
    return render_template('index.html')


def Calendar(date, time):
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    event_date = date + 'T' + time + ':00'

    event = {
        'summary': 'Hemodialysis Session',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': '',
        'start': {
            'dateTime': event_date,
            'timeZone': 'Africa/Cairo',
        },
        'end': {
            'dateTime': event_date,
            'timeZone': 'Africa/Cairo',
        },

        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    service = build('calendar', 'v3', credentials=creds)

    service.events().insert(calendarId='primary', body=event).execute()


app.run(port=5000, debug=True)
