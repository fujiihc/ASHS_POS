"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
#requirements removed: Flask~=1.1
import data as dt
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

df = dt.data(pd.read_csv('abCourseData.csv', encoding='cp1252').fillna('').astype(str))

#THINGS TO DO
#Remove AMPERSANS and SPECIAL CHARS in CSV w/o editing type
#Intro to IT has special characters
#Figure out what the hell the departments are
#Need to have a null display
#Need to have pages of results JS
#Fix that footer
#Find out what the Departments actually are

#Inconsistencies with inclusive modifiers being applied simultaneously

#eventually turn into environment variables or something
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_URL = 'https://accounts.google.com/.well-known/openid-configuration'

@app.route('/login')
def login():
    pass

@app.route('/login/callback')
def callback():
    pass

@app.route('/logout')
def logout():
    pass

#https://www.youtube.com/watch?v=FKgJEfrhU1E
#add google auth to create user database
#create custom requirements.txt file
#https://realpython.com/flask-google-login/
#https://console.cloud.google.com/apis/credentials?project=ashpos&supportedpurview=project
#how about asking the district for their actual google account
#saved under fujiihc, make sure to authorize Nileena and Davan as well


pathways = []
departments = []
courseLengths = []
courseLevels = []
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
    global departments
    global courseLengths
    global courseLevels
    global keyword
    
    if request.method == 'POST':
        #print(request.form)
            
        if request.form.get('searchButton') == '' and isinstance(request.form.get('searchBar'), str):
            keyword = request.form['searchBar']   
        elif request.form.get('origin') == 'pathways' and isinstance(request.form.get('selected'), str):
            pathways = request.form['selected'].split('#')
        elif request.form.get('origin') == 'departments' and isinstance(request.form.get('selected'), str):
            departments = request.form['selected'].split('#')
        elif request.form.get('origin') == 'courseLength' and isinstance(request.form.get('selected'), str):
            courseLengths = request.form['selected'].split('#')
        elif request.form.get('origin') == 'courseLevel' and isinstance(request.form.get('selected'), str):
            courseLevels = request.form['selected'].split('#')
        elif request.form.get('initialized') == 'initialized':
            return df.getDF().to_json()
        return search_w_modifiers(keyword)   

    return render_template('public_catalog.html')

def search_w_modifiers(keyword):
    global pathways
    global departments
    global courseLengths
    global courseLevels

    #should only be inclusive for the items contained within the inclusive modifier
    #exclusive to each other

    #inclusive = dt.data(pd.DataFrame())
    #for d in departments:
    #    if d != '':
    #        inclusive.merge(df.findCourse(d, 'dept'))
    #
    #for leng in courseLengths:
    #    if leng != '':
    #        inclusive.merge(df.findCourse(leng, 'Length'))
    #for lev in courseLevels:
    #    if lev != '':
    #        inclusive.merge(df.findCourse(lev, 'level'))

    #should be searching within the defined inclusive search
    #maybe compile a dataframe of possible candidates and then run a second search on them that is exclusive for all variables?
    

    #print(inclusive.getDF())
    #if len(inclusive.getDF()) == 0:
    #    toBeSearched = df
    #else:
    #    toBeSearched = inclusive

    #exclusive modifiers: only allows one to be checked at a time
    #it gets messy when you start having multiple modifiers within each category because there are so many "or"s
    #would it be easier to give them all the information possible?
    toBeSearched = df

    for p in pathways:
        if p != '':
            toBeSearched = toBeSearched.findCourse('X', p)
    
    for d in departments:
        if d != '':
            toBeSearched = toBeSearched.findCourse(d, 'dept')

    for leng in courseLengths:
        if leng != '':
            toBeSearched = toBeSearched.findCourse(leng, 'Length')

    for lev in courseLevels:
        if lev != '':
            toBeSearched = toBeSearched.findCourse(lev, 'level')

    #print(inclusive.getDF())
    #print(toBeSearched.getDF())
       
    pyResults = toBeSearched.findCourse(keyword.upper(), 'longDescription').getDF()
    print(pyResults)
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
    #create a user database
    return 'administrator access'

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
