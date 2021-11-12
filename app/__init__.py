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

from database import UsernamePasswordTable, BlogTable #using database classes


db_file = "tada.db"
#the conventional way:
#from flask import Flask, render_template, request

app = Flask(__name__)    #create Flask object
app.secret_key = os.urandom(32)

userpass = UsernamePasswordTable(db_file, "userpass")
blog = BlogTable(db_file, "blog")

@app.route("/",  methods=["GET", "POST"])
def disp_loginpage():
    if (session.get("username") is not None):
        # if there's an existing session, shows welcome page
        if request.method == "GET":
            # if there's an existing session, shows welcome page
            return render_template( 'response.html', username=session.get("username") )
        else:
            topic = request.form['topic']
            data = blog.seeContent()
            return render_template( 'response.html', username=session.get("username"), topic=topic, data=data )
    if ("username" != None):
        return render_template( 'login.html' )

@app.route("/viewselected")
def viewselected(topic, data):
    return render_template('viewselected.html', topic=topic, data=data)


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
        return redirect ("/")
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
        return redirect("/loggedin")
    elif (password!=passauth):
        return render_template('signup.html', passerror="Passwords must match")
    else:
        return render_template('signup.html', syntaxerror = "This username already exists")

@app.route("/loggedin")
def loggedin(): # does not show info in URL, shows /loggedin instead
    return redirect("/")


@app.route("/create", methods=["GET", "POST"])
def create():
    if session.get("username") is None:
        return redirect("/")

    if request.method == "GET":
        return render_template('create.html')
    else:
        topic = request.form['topic']
        username = session.get("username")
        title = request.form['title']
        post = request.form['postcontent']
        blog.insert(username, title, post, topic)

        return view(topic, title, post, blog.getNewestId())

@app.route("/edit/<int:id>",  methods=["GET", "POST"])
def edit(id):
    # temporary fix
    if not blog.idExists(id):
        return redirect("/create", 401)

    elif not blog.isAuthor(session.get("username"), id):
        return redirect(f"/view/{id}")
    elif request.method == "GET":
        data = blog.getEntryById(id)
        return editpost(data, id)
    else:
        topic = request.form['topic']
        title = request.form['title']
        post = request.form['postcontent']
        blog.updatePost(title, post, topic, id)

        # need template for success!
        return redirect(f"/view/{id}")

def editpost(data, id : int):
    return render_template('edit.html', post = data[3], title = data[2], topic = data[4], id=id)
#PREFILL TOPIC NOT WORKING :(

@app.route("/view")
def view(topic, title, post, id : int):
## where you can view the blogs
    return render_template('view.html', username=session.get("username"), title=title, post=post, topic=topic, id=id)


@app.route("/logout")
def logout():
    #if "username" in session:
    session["username"] = None
    session.pop("username", None)
    return redirect('/')


'''@app.route("/viewposts")
def posts():

    if session.get("username") is None:
        return redirect("/")

    return render_template("posts.html", matches=blog.seeContent())

''' # to be deleted developmental

@app.route("/view/<int:id>")
def viewpost(id):
    if session.get("username") is None:
        return redirect("/")

    blogContent = blog.getEntryById(id)
    return render_template("viewposts.html", title=blogContent[2],
                            post=blogContent[3],
                            #username=blogContent[1],
                            topic=blogContent[4],
                            id = blogContent[0],
                            canEdit=blog.isAuthor(session.get("username"), id)) #NOT FIXED NEED ERROR HANDLING TOOOO!!!!!
    # NEED TO FIX /VIEWPOSTS SO THAT IT DOESN'T CRASH IF THERE ARE NO POSTS!

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
