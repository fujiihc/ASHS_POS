"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

import data as dt
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, jsonify


app = Flask(__name__)

#have this built into somewhere else
#??what did i mean lmfao

df = dt.data(pd.read_csv('abCourseData.csv', encoding='utf8').fillna(''))
#probably came from the reformatting of the csv file in the git commit
#cp1252

#ask if daub can reset the course data except removing ampersands

pathways =[]
keyword = ''

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
    global pathways
    global keyword
    
    if request.method == 'POST':
    
    #need a better boolean to access the data. don't want it to be easily hackable
    #make sure that special characters are accounted for
            
        if request.form.get('searchButton') == "" and isinstance(request.form.get('searchBar'), str):

            keyword = request.form['searchBar']
            return search_w_modifiers(keyword)

        elif isinstance(request.form.get('selected'), str):

            pathways = request.form['selected'].split('#')
            return search_w_modifiers(keyword)

    return render_template('public_catalog.html')

def search_w_modifiers(keyword):
    global pathways
    toBeSearched = df      
    for p in pathways:
        if p != '':
            toBeSearched = toBeSearched.findCourse('X', p)
    pyResults = toBeSearched.findCourse(keyword.upper(), 'longDescription').getDF()
    return pyResults.to_json()

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
