from flask import Flask,jsonify,request,render_template

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysql",
    database="hosmansys"
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/PatientSignIn')
def PatientSignIn():
    return render_template('PatientSignIn.html')


@app.route('/PatientSignUp',methods=["GET","POST"])
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
        PatientPhone =  request.form['PatientPhone']
        PatientEmail = request.form['PatientEmail']
        PatientPass = request.form['PatientPass']
        sql = "INSERT INTO patients (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientHeight,PatientWeight,PatientBloodGrp,PatientPhone,PatientEmail,PatientPass) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (PatientFname,PatientLname,PatientGender,PatientBD,PatientSSN,PatientMaritalStat,PatientWeight,PatientBloodGrp,PatientHeight,PatientPhone,PatientEmail,PatientPass)
        mycursor.execute(sql,val)
        mydb.commit()
        return render_template('index.html')
    else:
        return render_template('PatientSignUp.html')


@app.route('/DoctorSignIn')
def DoctorSignIn():
    return render_template('DoctorSignIn.html')


@app.route('/DoctorSignUp')
def DoctorSignUp():
    return render_template('DoctorSignUp.html')


@app.route('/AdminSignIn')
def AdminSignIn():
    return render_template('AdminSignIn.html')


app.run(port=5000,debug=True)