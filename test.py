from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/PatientSignIn')
def PatientSignIn():
    return render_template('PatientSignIn.html')


@app.route('/PatientSignUp')
def PatientSignUp():
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


app.run(port=5000)
