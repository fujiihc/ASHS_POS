"""
This script runs the application using a development server.
It contains the definition of routes and views for the application. 
"""

from data import data
from database import database
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, session, abort, jsonify
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import GOOGLE_AUTH_URI
import httplib2
import json
import sqlite3

pathways = []
departments = []
courseLengths = []
courseLevels = []
cart = []
cartDF = data(pd.DataFrame())
keyword = ''
easterEgg = 'password1234'
isLoggedIn = False
global credentials

GOOGLE_CLIENT_ID = '415583783710-kpg937ob78e3ej719rldcf9or58d3vfa.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

db = database('database.db')
df = data(pd.read_csv('abCourseData.csv', encoding='cp1252').fillna('').astype(str))
oauthFlow = OAuth2WebServerFlow(client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET, scope = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'], redirect_uri='http://localhost:5555/oauth2callback', auth_uri=GOOGLE_AUTH_URI + '?hd=' + 'abington.k12.pa.us', revoke_uri='https://oauth2.googleapis.com/revoke')
#need a revoke uri which i use for logout?
app = Flask(__name__)


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#create a login checker for every route
@app.route('/login')
def login():
    return redirect(oauthFlow.step1_get_authorize_url())

@app.route('/logout')
def logout():
    
    global isLoggedIn
    global credentials
    isLoggedIn = False

    return redirect('/')
    #return redirect("https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=http://localhost:5555")

@app.route('/oauth2callback', methods = ['GET'])
def callback():
    global isLoggedIn
    global credentials
    credentials = oauthFlow.step2_exchange(request.args.get('code'))
    studentData = json.loads(credentials.to_json())
    
    print(studentData)
    try:
        if studentData['id_token']['hd'] == 'abington.k12.pa.us':
            isLoggedIn = True
            #this is where all of the login data should be updated and retrieved
            return redirect(url_for('student'))
    except:
        pass
    #include the revoke token here
    return redirect(url_for('login'))
    

@app.route('/', methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        if request.form.get('catalogButton'):
            return redirect(url_for('catalog'))
        elif request.form.get('studentAccess'):
            return redirect(url_for('login'))
        elif request.form.get('adminAccess'):
            return redirect(url_for('admin'))
        elif request.form.get('logoutBtn'):
            return redirect(url_for('logout'))
    return render_template('home.html')


@app.route('/catalog', methods = ['POST', 'GET'])
def catalog():
    global pathways
    global departments
    global courseLengths
    global courseLevels
    global keyword
    global easterEgg

    if request.method == 'POST':
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
        elif request.form.get('initialized') == '1' or request.form.get('clear') == 'true':
            pathways = []
            departments = []
            courseLengths = []
            courseLevels = []
            keyword = ''
            return df.getDF().to_json()
        elif request.form.get('logoutBtn'):
            return redirect(url_for('logout'))

        if keyword == easterEgg:
                return jsonify(dict(redirect='/credits'))

        return search_w_modifiers(keyword)   

    return render_template('public_catalog.html')

def search_w_modifiers(keyword):
    global pathways
    global departments
    global courseLengths
    global courseLevels

    toBeSearched = df

    for p in pathways:
        if p != '':
            toBeSearched = toBeSearched.findCourse('X', p, True)
    
    for d in departments:
        if d != '':
            toBeSearched = toBeSearched.findCourse(d, 'dept', True)
        #foundations of innovation
        #ap seminar and research
        #work study
    for leng in courseLengths:
        if leng != '':
            toBeSearched = toBeSearched.findCourse(leng, 'Length', True)

    for lev in courseLevels:
        if lev != '':
            toBeSearched = toBeSearched.findCourse(lev, 'level', True)

    pyResults = toBeSearched.findCourse(keyword.upper(), 'longDescription', False).getDF()
    return pyResults.to_json()

@app.route('/student', methods = ['POST','GET'])
def student():
    global isLoggedIn
    if isLoggedIn:
        global pathways
        global departments
        global courseLengths
        global courseLevels
        global keyword
        global cart
        global easterEgg
        global cartDF

        if request.method == 'POST':
            if request.form.get('editCart') == '':
                cart = request.form['cart'].split(',')
                cartDF = data(pd.DataFrame())
                for item in cart:
                    cartDF.merge(df.findCourse(item, 'longDescription', True))
                if request.form['redirect'] == 'true':
                    return jsonify(dict(redirect='/requests'))
            elif request.form.get('searchButton') == '' and isinstance(request.form.get('searchBar'), str):
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
            elif request.form.get('initialized') == '1' or request.form.get('clear') == 'true':
                pathways = []
                departments = []
                courseLengths = []
                courseLevels = []
                keyword = ''
                return {'data' : df.getDF().to_json(), 'cart' : cartDF.getDF().to_json()}
            elif request.form.get('logoutBtn'):
                return redirect(url_for('logout'))

            if keyword == easterEgg:
                    return jsonify(dict(redirect='/credits'))

            return search_w_modifiers(keyword)
        return render_template('student_access.html')
    else:
        return redirect(url_for('login'))

@app.route('/requests', methods = ['POST', 'GET'])
def requestsLink():
    global isLoggedIn
    if isLoggedIn:
        global cart
        global cartDF
        if request.method == 'POST':
            if request.form.get('logoutBtn'):
                return redirect(url_for('logout'))   
            elif request.form.get('initialized') == '1':
                cartDF = data(pd.DataFrame())
                for item in cart:
                    cartDF.merge(df.findCourse(item, 'longDescription', True))
                return cartDF.getDF().to_json()
            elif request.form.get('return') == '1':
                return jsonify(dict(redirect='/student'))
        return render_template('request_courses.html')
    else:
        return redirect(url_for('login'))

@app.route('/credits')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
