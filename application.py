# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 03:00:01 2020

@author: KennethJoel
"""


import os
import datetime

from flask import Flask, render_template, session, request, redirect
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import goodreads_review, comma

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET"])
def index():
    """Index page where users register"""

    # Render the main page-index
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """"Registration page"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # Ensure user name was submitted
        if not username:
            error = 'Please fill out username field.'
            return render_template("index.html", error=error)

        # Ensure password was submitted
        elif not password:
            error = 'Please fill out password field.'
            return render_template("index.html", error=error)

        # Check if username already exist
        if db.execute("SELECT * FROM customer WHERE username = :username", {"username" : request.form.get("username")}).rowcount == 1:
             error = 'User Name Already Exists!'
             return render_template("index.html", error=error)

        # Insert username and password(as a hash) into table users
        pw_hash = generate_password_hash(password)
        db.execute("INSERT INTO customer (username, password_hash, email, time_registered) VALUES (:username, :password_hash, :email, :time_registered)", {"username" : username, "password_hash" : pw_hash, "email" : email, "time_registered" : datetime.datetime.now()})

        db.commit()

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    
    user_name = request.form.get("username")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # flash('You are successfully logged in')

        # Ensure username was submitted
        if not user_name:
            error = 'Invalid Username and/or Password'
            return render_template("login.html", error=error)

        # Ensure password was submitted
        elif not request.form.get("password"):
            error = 'Invalid Username and/or Password'
            return render_template("login.html", error=error)

        # Query database for username
        rows = db.execute("SELECT * FROM customer WHERE username = :username", {"username" : user_name}).fetchall()
    
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
            error = 'Invalid Username and/or Password'
            return render_template("login.html", error=error)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/search")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Home page for book review site"""
    
    # Query for requested book in the database
    if 'user_id' in session:
        if request.method == "GET":
            return render_template("search.html")
        else:
            # Get form information.
            requested = request.form.get("search-books")
            search_book = '%'+requested+'%'
            
            # Ensure a request was submitted
            if not requested:
                return render_template("search.html", nonsuch='Please enter ISBN, title or author to be searched.')
            
            # Make sure the requested book exist
            if db.execute("SELECT * FROM book WHERE title ILIKE :title", {"title" : search_book}).rowcount == 0:
                return render_template("search.html", nonsuch='The Requested Book Is Not On The List')
            else:
                book_list = db.execute("SELECT * FROM book WHERE isbn LIKE :isbn OR title ILIKE :title OR author ILIKE :author", {"isbn" : search_book, "title" : search_book, "author" : search_book}).fetchall()
                
            # Getting Goodreads API information
            for i in range(len(book_list)):
                isbns = str(book_list[i]["isbn"])
                ratings_data = goodreads_review("0596009208")
            
            return render_template("search.html", book_list=book_list, ratings=comma(ratings_data["rate_count"]), average_ratings=isbns)
    else:
        return render_template("login.html")
    
@app.route("/book", methods=["POST"])
def book():
    """Book Page"""
    
    if 'user_id' in session:
        return render_template("book.html")
    else:
        return render_template("login.html")