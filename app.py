"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import data as dt
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, jsonify


app = Flask(__name__)

#have this built into somewhere else
df = dt.data()


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
       
        if request.form.get('pathway') or request.form.get('thingy'):                        
            print(request.form.getlist('pathway'))
            
            #need a better boolean to access the data. don't want it to be easily hackable
        elif request.form['searchButton'] == "":
            
            pySearched = request.form['searchBar']
            print(pySearched)
          
            pyResults = df.getCourse(pySearched.upper(), 'longDescription')
            pyLength = len(pyResults)
            #account for empty search
            #want to send data back to ajax where it will be processed in js 
            #return render_template('public_catalog.html', results = pyResults, ranges = range(pyLength), searched = pySearched, length = pyLength)
            #can't take a dataFrame as a return
            #dict, tuple, string
            return jsonify(pyResults.to_dict())
        

        #find a way to retain checkboxes
        #https://www.geeksforgeeks.org/flask-form-submission-without-page-reload/
        #use event listener and preventdefault??
        #maybe use the code from the link to ignore the pressing of the pathway dropdown buttons
     
    return render_template('public_catalog.html')

@app.route('/student', methods = ['POST','GET'])
def student():
    if request.method == 'POST':
        return redirect(url_for('requests'))
    return render_template('student_access.html')

#find a way to add individual students through authentication as well as add on request as a sub part of student
#this is just a simple fix
#something like /student/studentUSERNAME/requests
#maybe we just need to build like an authentication system or something
#remember to do subdomains

@app.route('/requests')
def requests():
    return render_template('request_courses.html')


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
