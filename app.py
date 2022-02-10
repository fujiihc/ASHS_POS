"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import course as cs
import data as dt
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)
turbo = Turbo(app)
#have this built into somewhere else
df = dt.data()
#this is tester code because we dont have the actual data file yet
c1 = cs.course('CS', '10101010', 'Literally computers and stuff like this', 5, 'Honors', 'Full Year', '10', 10)
df.addCourse(c1)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/', methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        if request.form.get('catalogButton'):
            return redirect(url_for('catalog'))
        elif request.form.get('studentAccess'):
            return redirect(url_for('student'))
        elif request.form.get('adminAccess'):
            return redirect(url_for('admin'))
    return render_template('home.html')



@app.route('/catalog', methods = ['POST', 'GET'])
def catalog():
    if request.method == 'POST':
        #find a way to differentiate the post get signals with buttons rather than inputs
        return render_template('public_catalog.html')
    return render_template('public_catalog.html')

@app.route('/student')
def student():
    return render_template('student_access.html')

@app.route('/admin')
def admin():
    #need to add google authentication in here somehow, which will then send information to the python script that'll store data somewhere?
    return 'administrator access'

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)

