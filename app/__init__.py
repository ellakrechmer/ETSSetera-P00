# ETSSetera: Shyne Choi, Ella Krechmer, Tina Nguyen, Sean+Patrick Ging
# SoftDev
# P00

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission
from flask import redirect          #facilitate URL redirecting
from flask import session

from random import *
import os
import sqlite3

from database import UsernamePasswordTable #import our class


db_file = "tada.db"
#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)

userpass = UsernamePasswordTable(db_file, "userpass")

@app.route("/") #, methods=['GET', 'POST'])
def disp_loginpage():
    if (session.get("username") is not None):
        # if there's an existing session, shows welcome page
       return render_template( 'response.html', username=session.get("username"))
    if ("username" != None):
        return render_template( 'login.html' )

@app.route("/login")
def login():
    username= request.args['username']
    password= request.args['password']

    if (username=="" or password==""):
        return render_template('login.html', syntaxerror="Cannot submit blank username or password")
    elif not userpass.userExists(username):
        return render_template('login.html', syntaxerror="Username does not exist")
    elif not userpass.passMatch(username, password):
        return render_template('login.html', syntaxerror = "Incorrect password")
    else:
        session["username"] = username
        return redirect('/loggedin')

@app.route("/signupdisplay")
def disp_signuppage():
    if (session.get("username") is not None):
        # if there's an existing session, shows welcome page
       return render_template( 'response.html', username=session.get("username"))
    if ("username" != None):
        return render_template( 'signup.html' )

@app.route("/signup")
def signup():
    username= request.args['username']
    password= request.args['password']
    passauth= request.args['passauth']
    if (username=="" or password==""):
        return render_template('signup.html', syntaxerror="Cannot submit blank username or password")
    elif not userpass.userExists(username):
        userpass.insert(username, password) # committing actions to database must be done every time you commit a command
        session["username"]=username
        return redirect('/loggedin')
    elif (password!=passauth):
        return render_template('signup.html', passerror="Passwords must match")
    else:
        return render_template('signup.html', syntaxerror = "This username already exists")


@app.route("/loggedin")
def loggedin(): # does not show info in URL, shows /loggedin instead
    return render_template( 'response.html', username=session.get("username"))


@app.route("/logout")
def logout():
    #if "username" in session:
    session["username"] = None
    session.pop("username", None)
    return redirect('/')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
