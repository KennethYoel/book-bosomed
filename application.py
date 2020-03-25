# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 03:00:01 2020

@author: KennethJoel
"""


import os
import datetime
import untangle

from flask import Flask, render_template, session, request, redirect, jsonify
from flask_session import Session

from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import goodreads_review, commaSeparator

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
        customer_rows = db.execute("SELECT * FROM customer WHERE username = :username", {"username" : user_name}).fetchall()
    
        # Ensure username exists and password is correct
        if len(customer_rows) != 1 or not check_password_hash(customer_rows[0]["password_hash"], request.form.get("password")):
            error = 'Invalid Username and/or Password'
            return render_template("login.html", error=error)

        # Remember which user has logged in
        session["user_id"] = customer_rows[0]["id"]

        # Redirect user to search page
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
            book_rows = db.execute("SELECT * FROM book WHERE isbn LIKE :isbn OR title ILIKE :title OR author ILIKE :author", {"isbn" : search_book, "title" : search_book, "author" : search_book})
            if book_rows.rowcount == 0:
                return render_template("search.html", nonsuch='The Requested Book Is Not On The List')
            else:
                temp_list = book_rows.fetchall()
                ratings = goodreads_review(temp_list[0]["isbn"])
                book_list = [(dict(id=temp_list[0]["id"], isbn=temp_list[0]["isbn"], title=temp_list[0]["title"], author=temp_list[0]["author"], year=temp_list[0]["year"], rate_average=ratings["rate_average"], rate_count=commaSeparator(ratings["rate_count"])))]
                
                # Add the db information and goodreads api to book_list
                for i in range(1, len(temp_list)):
                    # Getting Goodreads API information
                    ratings = goodreads_review(temp_list[i]["isbn"])
                    if ratings == None:
                        total_ratings = 0
                        average_ratings = 0.0
                    else:
                        total_ratings = commaSeparator(ratings["rate_count"])
                        average_ratings = ratings["rate_average"]
                        
                    book_list.append(dict(id=temp_list[i]["id"], isbn=temp_list[i]["isbn"], title=temp_list[i]["title"], author=temp_list[i]["author"], year=temp_list[i]["year"], rate_average=average_ratings, rate_count=total_ratings))
                    
            return render_template("search.html", book_list=book_list)
    else:
        return render_template("login.html")

    
@app.route("/book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    """Book Page"""
    
    if 'user_id' in session:
        # Get book information
        the_book = db.execute("SELECT * FROM book WHERE id = :id", {"id" : book_id}).fetchall()
        
        # Get book reviews information
        review_list = db.execute("SELECT rating, book_review, book_id, username, customer_id, customer.id FROM review JOIN customer ON review.customer_id = customer.id WHERE book_id = :id", {"id" : book_id}).fetchall()
        
        # Get username for the customer db
        customer_name = db.execute("SELECT username FROM customer WHERE id = :id", {"id" : session["user_id"]}).fetchone()
        
        # Getting Goodreads API information
        rating_results = goodreads_review(the_book[0]["isbn"])
        if rating_results == None:
            total_ratings = 0
            average_ratings = 0.0
        else:
            total_ratings = commaSeparator(rating_results["rate_count"])
            average_ratings = rating_results["rate_average"]
            
        # Get xml data from goodreads api   
        doc = untangle.parse(f'https://www.goodreads.com/book/isbn/{the_book[0]["isbn"]}?key=GZZX52IAd0zxYaYnZOsw')
        description = doc.GoodreadsResponse.book.description.cdata
        cover_img = doc.GoodreadsResponse.book.image_url.cdata
        
        if request.method == "POST":
            # Readers review
            book_rating = request.form.get("book_rating")
            book_review = request.form.get("reader_review")
            
            if not book_rating:
                book_rating = 0
                
            if not book_review:
                book_review = ""
            
            # Make sure a posted review by the user doesn't already exist for the book requested before inserting it into db.
            review_rows = db.execute("SELECT book_id FROM review WHERE customer_id = :customer_id", {"customer_id" : session["user_id"]}).fetchall();
            if len(review_rows) != 1:
                db.execute("INSERT INTO review (rating, book_review, book_id, customer_id) VALUES (:rating, :book_review, :book_id, :customer_id)", {"rating" : book_rating, "book_review" : book_review, "book_id" : book_id, "customer_id" : session["user_id"]})
            elif review_rows[0]["book_id"] != book_id:
                db.execute("INSERT INTO review (rating, book_review, book_id, customer_id) VALUES (:rating, :book_review, :book_id, :customer_id)", {"rating" : book_rating, "book_review" : book_review, "book_id" : book_id, "customer_id" : session["user_id"]})
            db.commit()
            
            return render_template("book.html", customer_name=customer_name["username"], review_list=review_list, book_id=the_book[0]["id"], the_title=the_book[0]["title"], the_author=the_book[0]["author"], the_year=the_book[0]["year"], the_isbn=the_book[0]["isbn"], total_ratings=total_ratings, average_ratings=average_ratings, cover_img=cover_img, description=description)
        
        else:
            return render_template("book.html", customer_name=customer_name["username"], review_list=review_list, book_id=the_book[0]["id"], the_title=the_book[0]["title"], the_author=the_book[0]["author"], the_year=the_book[0]["year"], the_isbn=the_book[0]["isbn"], total_ratings=total_ratings, average_ratings=average_ratings, cover_img=cover_img, description=description)
    else:
        return render_template("login.html")
  
    
@app.route("/api/<string:isbn>", methods=["GET"])
def book_api(isbn):
    """Return details book’s title, author, publication date, ISBN number, review count, and average score."""
    
    # Make sure the requested book exists.
    the_book = db.execute("SELECT * FROM book WHERE isbn = :isbn", {"isbn" : isbn})
    if the_book is None:
        return jsonify({"error": "Invalid book_api"}), 404
    
    # Get all the book information.
    pages = the_book.fetchall()
    
    # Calculate the sum and average of the user's rating's and then insert into review.
    rating_total = db.execute("SELECT COALESCE(SUM(rating),0) AS rating_total FROM review WHERE book_id = :book_id;", {"book_id" : pages[0]["id"]}).fetchone()
    rating_avg = db.execute("SELECT COALESCE(AVG(rating),0) AS rating_avg FROM review WHERE book_id = :book_id;", {"book_id" : pages[0]["id"]}).fetchone()
    db.execute("UPDATE book SET rate_count = :rate_count, rate_average = :rate_average WHERE id = :id", {"rate_count" : rating_total[0], "rate_average" : rating_avg[0], "id" : pages[0]["id"]})
    
    db.commit()
    
    return jsonify({
            "title": pages[0]["title"],
            "author": pages[0]["author"],
            "publication_date": pages[0]["year"],
            "ISBN": pages[0]["isbn"],
            "review_count" : pages[0]["rate_count"],
            "average_score" : pages[0]["rate_average"]
            })