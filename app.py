from flask import Flask, render_template, request,  send_file
import pandas as pd
import matcher as mr

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    """Serve homepage template."""
    return render_template('index.html')

@app.route("/results", methods=["GET","POST"])
def run():
    if request.method == 'POST':
        drivers = request.files['drivers']
        wRiders = request.files['wRiders']
        pRiders = request.files['pRiders']
        df = pd.read_csv(drivers)
        wrf = pd.read_csv(wRiders)
        prf = pd.read_csv(pRiders)
        process(df, wrf, prf)
        return render_template('results.html', message="Files uploaded")
    return render_template('error.html', message="Error")

#Process the provided forms and create the needed CSVs
def process(df, wrf, prf):
    mr.setupDf(df)
    mr.sort(df, prf)
    df_copy = mr.simplifyDf(df)
    rf = mr.combineRiders(wrf, prf)
    mr.assign(df, df_copy, rf)
    mr.getAssignments(rf)
    mr.getDrivers(df)

#Download driver-rider assignments as a CSV
@app.route("/download_assignments", methods=["GET", "POST"])
def download_assignments():
    return send_file("assignments.csv", as_attachment=True)

#Download the updated drivers CSV
@app.route("/download_drivers", methods=["GET", "POST"])
def download_drivers():
    return send_file("drivers.csv", as_attachment=True)