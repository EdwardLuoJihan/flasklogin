from flask import Flask, render_template, redirect, url_for, request, session
import json
from datetime import timedelta
import random

app = Flask(__name__)
app.secret_key = 'thisisakey'

COLORS = [
    ['#DF7FD7', '#DF7FD7', '#591854'],
    ['#E3CAC8', '#DF8A82', '#5E3A37'],
    ['#E6845E', '#E05118', '#61230B'],
    ['#E0B050', '#E6CB97', '#614C23'],
    ['#9878AD', '#492661', '#C59BE0'],
    ['#787BAD', '#141961', '#9B9FE0'],
    ['#78A2AD', '#104F61', '#9BD1E0'],
    ['#78AD8A', '#0A6129', '#9BE0B3'],
    ['#AD8621', '#6B5621', '#E0AD2B'],
]

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')
def index():
    try:
        f = open('users.json')
        users = json.load(f)
        if session['username'] != None:
            return render_template('index.html', username=session['username'], colors=users[session['username']]['c'])
    except:
        return render_template('index.html', username="Guest", colors=['#d6d6d6','#d6d6d6','#d6d6d6'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        f = open('users.json')
        users = json.load(f)
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['p']:
            session['username'] = username
            return redirect(url_for('index'))
        elif username == 'admin' and username == 'admin':
            session[username] = password
            return redirect(url_for('admin'))
        error = "Invalid Credentials. Please try again."
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        f = open('users.json')
        users = json.load(f)
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        if username in users:
            error = "This username is taken, please try another."
        elif password == '' or username == '' or name == '':
            error = "Empty field(s)."
        else:
            color = random.choice(COLORS)
            users[username] = {'name': name, 'p': password, 'c': color}
            with open('users.json', 'w') as f:
                json.dump(users, f)
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('signup.html', error=error)

@app.route('/signout')
def signout():
    session.pop('username', default=None)
    return redirect(url_for('index'))

app.run()