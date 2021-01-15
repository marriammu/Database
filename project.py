from flask import Flask, request, render_template, url_for, redirect, session, flash
from werkzeug.utils import secure_filename
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


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    mycursor.execute("CREATE TABLE patients (PatientFname VARCHAR(50),PatientLname VARCHAR(50),PatientGender ENUM('Female','Male'),PatientBD VARCHAR(50),PatientSSN VARCHAR(50),PatientMaritalStat ENUM('Single','Married','Widowed','Divorced'),PatientHeight VARCHAR(50),PatientWeight VARCHAR(50),PatientBloodGrp VARCHAR(5),PatientPhone VARCHAR(50),PatientEmail VARCHAR(250) NOT NULL UNIQUE,PatientPass VARCHAR(50)")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('doctors',):
        y = False
if y:
    mycursor.execute("CREATE TABLE doctors (DoctorFName VARCHAR(50),DoctorMName VARCHAR(50),DoctorLName VARCHAR(50),DoctorAddress VARCHAR(250),DoctorNationality VARCHAR(25),DoctorGender VARCHAR(25),DoctorBD VARCHAR(50),DoctorSSN VARCHAR(250),DoctorMaritalStat ENUM('Single','Married','Widowed','Divorced'),DoctorPhone VARCHAR(50),DoctorBankNum VARCHAR(50),DoctorEmpDate VARCHAR(50),DoctorSalary VARCHAR(50),DoctorShift VARCHAR(50),DoctorEmail VARCHAR(250) ,DoctorPass VARCHAR(50))")

mycursor.execute("SHOW TABLES")
y = True
for x in mycursor:
    if x == ('appointments',):
        y = False
if y:
    mycursor.execute("CREATE TABLE appointments (PatientFname VARCHAR(50),PatientEmail VARCHAR(50),DoctorEmail VARCHAR(50),AppointmentDate VARCHAR(50),AppointmentTime VARCHAR(50),Doctorname VARCHAR(50))")

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
        "CREATE TABLE testresults (TestName VARCHAR(50),TestDate VARCHAR(50),TestFile VARCHAR(333))")

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
# @app.route('/PatientSignIn', methods=["GET", "POST"])
# def PatientSignIn():
#     if request.method == "POST":
#         PatientUserName = request.form['SignInPatientUsername']
#         PatientPasswd = request.form['SignInPatientPassword']
#         mycursor.execute("SELECT * FROM patients WHERE PatientEmail = %s AND PatientPass = %s ",(PatientUserName, PatientPasswd))
#         email = mycursor.fetchone()
#         if email:
#             session['loggedin'] = True
#             session['id'] = PatientUserName
#             session['username'] = PatientUserName
#             return render_template('PatientPanel.html')
#         else:
#             return render_template('PatientSignIn.html', er='Incorretct Email or Password')
#     else:
#         return render_template('PatientSignIn.html')


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
        # print(Patientemail)
        for x in patientE:
            # print(x[0])
            if x[0] == Patientemail:
                # print(x[0])
                return render_template('PatientSignUp.html', msg='Email is already exist')
            else:
                continue
        if Patientpass != ConfirmPatientPass:
            return render_template('PatientSignUp.html', msg="Password doesn't match")    
        else:
            sql = "INSERT INTO patients (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (Patientfirstname, Patientlastname, Patientgender, Patientbirthdate, Patientssn, Patientmaritalstat,
               Patientheight, Patientweight, Patientbloodgrp, Patientphone, Patientemail, Patientpass)
            mycursor.execute(sql, val)
        # print(Patientemail)
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
    if 'type' in session =='patient':
        mycursor.execute(
            "SELECT * FROM  patients WHERE PatientEmail = %s ", (session['username'],))
        email = mycursor.fetchone()
        return render_template('ViewPatientProfile.html', data=email)
    else:
        return render_template('PatientSignIn.html',er='PLEASE SIGN IN')    



@app.route('/PatientPanel/UpdatePatientProfile', methods=['POST', 'GET'])
def UpdatePatientProfile():
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
        data1=[PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass]
        sql = "UPDATE patients SET PatientFname=%s,PatientLname=%s,PatientGender=%s,PatientBD=%s,PatientSSN=%s,PatientMaritalStat=%s,PatientHeight=%s,PatientWeight=%s,PatientBloodGrp=%s,PatientPhone=%s,PatientEmail=%s,PatientPass=%s"
        val = (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass)
        mycursor.execute(sql,val)
        mydb.commit()
        
        return render_template('UpdatePatientProfile.html', data=patientdata, msg='YOU UPDATED YOUR PROFILE SUCCESSFULLY')
    else:
        mycursor.execute("SELECT *FROM  patients WHERE PatientEmail = %s ", (session['username'],))
        patientdata = mycursor.fetchone()
        return render_template('UpdatePatientProfile.html', data=patientdata)


@app.route('/PatientPanel/PatientViewShifts')
def PatientViewShifts():
    mycursor.execute("SELECT DoctorFName, DoctorMName, DoctorShift FROM doctors")
    data = mycursor.fetchall()
    return render_template("PatientViewShifts.html", appoint=data)


@app.route('/PatientPanel/PatientAddAppoint', methods=['POST', 'GET'])
def PatientAddAppoint():
    if request.method == 'POST':
        AppointmentDate = request.form['PatientApointDay']
        AppointmentTime = request.form['PatientApointTime']
        Doctorname = request.form['PatientApointDoc']
        mycursor.execute(
        "SELECT PatientFname FROM  patients WHERE PatientEmail = %s ", (session['username'],))
        Patient_name = mycursor.fetchone()
        sql = "INSERT INTO appointments (PatientFname,AppointmentDate,AppointmentTime,Doctorname,PatientEmail) VALUES (%s,%s,%s,%s,%s)"
        val = (Patient_name[0],AppointmentDate, AppointmentTime, Doctorname,session['username'])
        mycursor.execute(sql, val)
        mydb.commit()
        Calendar(AppointmentDate,AppointmentTime)
        return render_template('PatientViewAppoints.html')
    else:
        return render_template('PatientAddAppoint.html')


@app.route('PatientPanel/PatientViewAppoints')
def PatientViewAppoints():
    mycursor.execute("SELECT AppointmentDate AppointmentTime Doctorname FROM appointments WHERE PatientEmail = %s ", (session['username'],))
    data = mycursor.fetchall()
    return render_template('PatientViewAppoints.html', app=data)


# def save_file(f):
#     hash_f=secrets.token_urlsafe(10)
#     __, file_extention = os.path.splitext(f.filename)
#     f_name = hash_f + file_extention
#     file_path = os.path.join(app.root_path, 'static/img', f_name)
#     f.save(file_path)
#     return f_name


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/PatientPanel/PatientAddTestResults', methods=['POST', 'GET'])
def PatientTestResults():
    if request.method == 'POST':
        TestName = request.form['TestName']
        TestDate = request.form['TestDate']
        TestFile = request.files['TestFile']
        url = TestFile.save(secure_filename(TestFile.filename))
        print(url)

        #TestFile = save_file(secure_filename(request.files['TestFile']))
        # if 'TestFile' not in request.files:
        #     flash('No file part')
        #     return render_template('PatientAddTestResults.html',msg='No file part')
        
        # if TestFile.filename == '':
        #     flash('No selected file')
        #     return render_template('PatientAddTestResults.html',msg='NO FILUPLOADEDE IS')
        # if TestFile and allowed_file(TestFile.filename):
        #     filename = secure_filename(TestFile.filename)
        #     TestFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     url = url_for('uploaded_file',filename=filename)
        #     print(url)
        
        sql = "INSERT INTO testresults (TestName,TestDate,TestFile) VALUES (%s,%s,%s)"
        val = (TestName,TestDate,url)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('PatientAddTestResults.html')
    else:
        return render_template('PatientAddTestResults.html')


@app.route('/PatientPanel/PatientViewTestResults')
def PatientViewTestResults():
    mycursor.execute("SELECT *FROM testresults")
    data = mycursor.fetchall()
    return render_template('PatientViewTestResults.html', TestData=data)


@app.route('/PatientPanel/PatientContactUs', methods=['POST', 'GET'])
def PatientContactUs():
    if request.method == 'POST':
        PatientContactUs = request.form['PatientContactUs']
        mycursor.execute("SELECT PatientFname FROM patients WHERE PatientEmail = %s ", (session['username'],))
        data1 = mycursor.fetchone()
        mycursor.execute("SELECT PatientLname FROM patients WHERE PatientEmail = %s ", (session['username'],))
        data2 = mycursor.fetchone()
        print(data1[0])
        print(data2[0])
        sql = "INSERT INTO feedback (PatientFname,PatientLname,PatientEmail,PatientContactUs) VALUES (%s,%s,%s,%s)"
        val = (data1[0],data2[0],session['username'],PatientContactUs)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('/PatientContactUs.html')
    else:
        return render_template('/PatientContactUs.html')



@app.route('/PatientPanel/PatientMedicalHistory',methods=['POST','GET'])
def PatientMedicalHistory():
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
        print(data1[0])
        print(data2[0])  
        sql = "INSERT INTO medicalhistory (PatientFname,PatientLname,PatientEmail,ChronicDisease,Prescription,EmergencyMed,Alergies,SurgicalHistory,Fracture,Smoker) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (data1[0],data2[0],session['username'],ChronicDisease,Prescription,EmergencyMed,Alergies,SurgicalHistory,Fracture,Smoker)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('/PatientMedicalHistory.html')
    else:
        return render_template('/PatientMedicalHistory.html')


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
        print(request)
        # print(request.form)
        UserName = request.form['SignInAdminUsername']
        Pass = request.form['SignInAdminPassword']
        if UserName == 'Admin@hos' and Pass == '1234':
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
        mycursor.execute("SELECT DoctorEmail FROM doctors")
        DoctorE = mycursor.fetchall()
        print(DoctorE)
        for x in DoctorE:
            print(x)
            if x[0] == Email:
                print(x[0])
                return render_template('AddDoctor.html', msg='Email is already exist')
            else:
                continue
        sql = "INSERT INTO doctors (DoctorFName,DoctorMName,DoctorLName,DoctorAddress,DoctorNationality,DoctorGender,DoctorBD,DoctorSSN,DoctorMaritalStat,DoctorPhone,DoctorBankNum,DoctorEmpDate,DoctorSalary,DoctorShift,DoctorEmail,DoctorPass) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (Fname, Mname, Lname, Address, Nationality, Gender,
               BD, SSN, MaritalStat, Phone, BankNum,DoctorEmpDate ,  DoctorSalary, DoctorShift, Email,Pass)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('AdminPanel.html', msg='DOCTOR ADDED SUCCESSFULLY')
        # return AdminPanel()
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
        return redirect(url_for('AdminPanel'))
    else:
        return render_template('AddDevice.html')
        
@app.route('/AdminPanel/AdminUpdate', methods=['POST', 'GET'])
def AdminUpdate():
    if request.method == 'POST':
        DeviceSerialNo = request.form['DeviceSerialNo']
        DeviceBrand = request.form['DeviceBrand']
        TotalDialysis = request.form['TotalDialysis']
        LastMaint = request.form['LastMaint']
        NextMaint = request.form['NextMaint']
        sql = "INSERT INTO devices (DeviceSerialNo,DeviceBrand,TotalDialysis,LastMaint,NextMaint) VALUES (%s,%s,%s,%s,%s)"
        val = (DeviceSerialNo, DeviceBrand,
               TotalDialysis, LastMaint, NextMaint)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template('AdminUpdate.html')
    else:
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

@app.route('/AdminPanel/StatisticalAnalysis')
def StatisticalAnalysis():
    mycursor.execute("SELECT DoctorSSN FROM doctors" )
    DoctorSSNs = mycursor.fetchall()
    DoctorsNum=len(DoctorSSNs)
    mycursor.execute("SELECT PatientSSN FROM patients" )
    PatientSSN = mycursor.fetchall()
    PatientsNum=len(PatientSSN)
    mycursor.execute("SELECT DeviceSerialNo FROM devices" )
    DeviceSerialNum = mycursor.fetchall()
    DevicesNumber=len(DeviceSerialNum)
    mycursor.execute("SELECT AppointmentTime FROM appointments" )
    Appointment = mycursor.fetchall()
    Appointments =len(Appointment)
    labels=['Doctors','Patients','Devices','Appointments']

    values=[DoctorsNum,PatientsNum,DevicesNumber,Appointments]
    return render_template('StatisticalAnalysis.html') 
   

@app.route('/SignOut')
def logout():
    session.clear()
    return render_template('index.html')




# def Calendar(date,time):
#     SCOPES = ['https://www.googleapis.com/auth/calendar']

#     """Shows basic usage of the Google Calendar API.
#     Prints the start and name of the next 10 events on the user's calendar.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'secrets.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     event_date = date + 'T' + time + ':00'

#     event = {
#     'summary': 'Hemodialysis Session',
#     'location': '800 Howard St., San Francisco, CA 94103',
#     'description': '',
#     'start': {
#         'dateTime': event_date,
#         'timeZone': 'Africa/Cairo',
#     },
#     'end': {
#         'dateTime': event_date,
#         'timeZone': 'Africa/Cairo',
#     },
    
#     'reminders': {
#         'useDefault': False,
#         'overrides': [
#         {'method': 'email', 'minutes': 24 * 60},
#         {'method': 'popup', 'minutes': 10},
#         ],
#     },
#     }
#     service = build('calendar', 'v3', credentials=creds)

#     service.events().insert(calendarId='primary', body=event).execute()



app.run(port=5000, debug=True)
