# ETSSetera: Shyne Choi, Ella Krechmer, Tina Nguyen, Sean Ging
# SoftDev
# P00

from flask import Flask             #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request           #facilitate form submission


from random import *
import os
import sqlite3

db_file = "tada.db"
#the conventional way:
#from flask import Flask, render_template, request

from flask import session
app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)
userpass = sqlite3.connect(db_file, check_same_thread=False)
c= userpass.cursor()
c.execute("DROP TABLE IF EXISTS userpass")
c.execute("CREATE TABLE userpass(username TEXT, password TEXT);" )

@app.route("/") #, methods=['GET', 'POST'])
def disp_loginpage():
    # print("\n\n\n")
    # print("***DIAG: request.args['username']  ***")
    # print(request.args['username'])
    # print("***DIAG: request.args['password']  ***")
    # print(request.args['password'])
    if ("username" != None):
        return render_template( 'login.html' )

@app.route("/signup")
def signup():
    username= request.args['username']
    password= request.args['password']
    passauth= request.args['passauth']
    command=f"""INSERT INTO userpass VALUES("{username}", "{password}");"""
    c.execute(command)
    # c.execute("SELECT username from userpass;")
    # for row in c.execute("SELECT username from userpass;"):
    #     if(row != username):
    #         c.execute('INSERT INTO userpass VALUES (username, password);')
    #         return render_template('response.html')
    #     else:
    #         return render_template('login.html', error="username already exists")

    if (username=="" or password==""):
        return render_template('login.html', syntaxerror="Cannot submit blank username or password")
    elif (password!=passauth):
        return render_template('login.html', passerror="Passwords must match")
    else:
        return render_template('response.html', username=username)

@app.route("/logout")
def logout():
    #if "username" in session:
    session["username"] = None
    session.pop("username", None)
    return render_template('login.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
