"""
This script runs the application using a development server.
It contains the definition of routes and views for the application. 
"""
#added extra requirements
#https://stackoverflow.com/questions/12909332/how-to-logout-of-an-application-where-i-used-oauth2-to-login-with-google
 

import data as dt
import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, session, abort, jsonify
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import GOOGLE_AUTH_URI
import json

app = Flask(__name__)
df = dt.data(pd.read_csv('abCourseData.csv', encoding='cp1252').fillna('').astype(str))


#https://github.com/lepture/flask-oauthlib/blob/master/example/google.py

GOOGLE_CLIENT_ID = '415583783710-kpg937ob78e3ej719rldcf9or58d3vfa.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'

auth_uri = GOOGLE_AUTH_URI + '?hd=' + 'abington.k12.pa.us'
auth_flow = OAuth2WebServerFlow(client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET, scope = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'], redirect_uri='http://localhost:5555/oauth2callback', auth_uri=auth_uri)

#https://stackoverflow.com/questions/37748993/authenticate-user-with-a-specific-hosted-domain-hd-in-flask-with-oauth2
#https://stackoverflow.com/questions/10664868/where-can-i-find-a-list-of-scopes-for-googles-oauth-2-0-api
#https://stackoverflow.com/questions/21463869/multiple-scopes-using-oauth2webserverflow

#https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask

#https://oauth2client.readthedocs.io/_/downloads/en/latest/pdf/
#page 22 flask
#page 31 for oauth2webserverflow

@app.route('/login')
def login():
    return redirect(auth_flow.step1_get_authorize_url())

@app.route('/logout')
def logout():
    return redirect('/')


@app.route('/oauth2callback', methods = ['GET'])
def callback():
    studentData = json.loads(auth_flow.step2_exchange(request.args.get('code')).to_json())
    #gotta like authorize this or something idrk
    if studentData['id_token']['hd'] == 'abington.k12.pa.us':
        return redirect(url_for('student'))
    return redirect(url_for('login'))
    
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
cart = []
cartDF = dt.data(pd.DataFrame())
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
            return df.getDF().to_json()
        elif request.form.get('logoutBtn'):
            return redirect(url_for('logout'))
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

    #print(inclusive.getDF())
    #print(toBeSearched.getDF())
       
    pyResults = toBeSearched.findCourse(keyword.upper(), 'longDescription', False).getDF()
    #print(pyResults)
    return pyResults.to_json()

#make sure that this checks for login
#login checker is not working

@app.route('/student', methods = ['POST','GET'])
def student():
    global pathways
    global departments
    global courseLengths
    global courseLevels
    global keyword
    global cart

    if request.method == 'POST':
        if request.form.get('editCart') == '':
            cart = request.form['cart'].split(',')
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
            return {'data' : df.getDF().to_json(), 'cart' : cartDF.getDF().to_json()}
        elif request.form.get('logoutBtn'):
            return redirect(url_for('logout'))
        return search_w_modifiers(keyword)
    return render_template('student_access.html')
#remember to do subdomains


@app.route('/requests', methods = ['POST', 'GET'])
def requests():
    global cart
    global cartDF
    if request.method == 'POST':
        if request.form.get('logoutBtn'):
            return redirect(url_for('logout'))   
        elif request.form.get('initialized') == '1':
            cartDF = dt.data(pd.DataFrame())
            for item in cart:
                cartDF.merge(df.findCourse(item, 'longDescription', True))
            return cartDF.getDF().to_json()
        elif request.form.get('return') == '1':
            return jsonify(dict(redirect='/student'))
    return render_template('request_courses.html')

#kinda scuffed atm
@app.route('/admin')
def admin():
    return 'administrator access'

#https://medium.com/swlh/hacking-flask-applications-939eae4bffed
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
