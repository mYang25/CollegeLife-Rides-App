# CL-Rides-App
Guide for setting up and running the CL Rides App locally.

## Create & Configure the Virtual Environment
1. Create the virtual environment
    - `python3 -m venv venv`
2. Activate your virtual environment
    - `source venv/bin/activate`
   </br>Or for Windows
    - `cd venv\Scripts`
    - `.\activate.bat`
3. Install the dependencies
    - `pip install -r requirements.txt`

## Run the Application Locally
1. (Optional but recommended) Set the `FLASK_ENV` environment variable
    - `export FLASK_ENV=development`
    - This setting enables automatic reloads so you don't have to restart the server each time you make changes, just refresh the page.
5. Run the application
    - `flask run`
   </br>Or for Windows
    - `cd C:User\filepath\CL-Rides-Pog`
    - `set FLASK_ENV=development`
    - `set FLASK_APP=app`
    - `flask run`
