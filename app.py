"""
This script runs the application using a development server.
It contains the definition of routes and views for the application. 
"""
#requirements removed: Flask~=1.1
#added extra requirements
import os
import pathlib
import requests as rq
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

import data as dt
import database as db
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, session, abort

app = Flask(__name__)

df = dt.data(pd.read_csv('abCourseData.csv', encoding='cp1252').fillna('').astype(str))

studentInfo = db.database()

#need a way to register logins. Once logged in, need to store student data in the database, and then pass relevant info in Ajax call to the html
#need a way to handle simultaneous requests. Can't have "current user" create a user class in order to deal with multiple users at once and store their data easily
#https://google-auth.readthedocs.io/en/stable/index.html
#https://geekyhumans.com/how-to-implement-google-login-in-flask-app/#more-20670

#THINGS TO DO
#Need to have a null display
#Fix that footer


#Inconsistencies with inclusive modifiers being applied simultaneously

#eventually turn into environment variables or something
#import oshttps://www.geeksforgeeks.org/read-json-file-using-python/
#os.getenv
app.secret_key = 'testKey'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#need a way to grab the file. Just place it in the same directory and grab it?

#maybe create OS ENV variables rather than storing them in a file
#if not, test for file access exploits
GOOGLE_CLIENT_ID = '415583783710-kpg937ob78e3ej719rldcf9or58d3vfa.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
#could use to edit scopes later on
GOOGLE_URL = 'https://accounts.google.com/.well-known/openid-configuration'

client_secrets_file = os.path.join(pathlib.Path(__file__).parent, 'client.json')
#edit the scopes
flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"], redirect_uri = 'http://localhost:5555/callback')

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if 'google_id' not in session:
            return abort(401)
        else:
            return function()
    return wrapper

@app.route('/login')
def login():
    authorization_url,state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)
    
@app.route('/callback')
def callback():
    #callback function
    #redirects to student access
    #also loads and saves student session info
    flow.fetch_token(authorization_response = request.url)

    #if not session['state'] == request['state']:
    #    abort(500)

    credentials = flow.credentials
    request_session = rq.sessions.Session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session = cached_session)
    id_info = id_token.verify_oauth2_token(id_token = credentials._id_token, request = token_request, audience = GOOGLE_CLIENT_ID)
    session['google_id'] = id_info.get('sub')
    session['name'] = id_info.get('name')
    return redirect(url_for('student'))

@app.route('/credits')
def credits():
    return render_template('credits.html')

#https://www.youtube.com/watch?v=FKgJEfrhU1E
#add google auth to create user database
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
            return redirect(url_for('login'))
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
            keyword = request.form['searchBar']
        elif request.form.get('origin') == 'departments' and isinstance(request.form.get('selected'), str):
            departments = request.form['selected'].split('#')
            keyword = request.form['searchBar']
        elif request.form.get('origin') == 'courseLength' and isinstance(request.form.get('selected'), str):
            courseLengths = request.form['selected'].split('#')
            keyword = request.form['searchBar']
        elif request.form.get('origin') == 'courseLevel' and isinstance(request.form.get('selected'), str):
            courseLevels = request.form['selected'].split('#')
            keyword = request.form['searchBar']
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
    
    #make secondary modifiers inclusive
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
    #print(pyResults)
    return pyResults.to_json()

#make sure that this checks for login
@login_is_required
@app.route('/student', methods = ['POST','GET'])
def student():
    if request.method == 'POST':
        return redirect(url_for('requests'))
    return render_template('student_access.html')
#remember to do subdomains

@login_is_required
@app.route('/requests')
def requests():
    return render_template('request_courses.html')

#kinda scuffed atm
@app.route('/admin')
def admin():
    return 'administrator access'

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
