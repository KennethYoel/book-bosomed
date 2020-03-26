# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:21:10 2020

@author: KennethJoel
"""


import requests
import os

from flask import render_template, session, redirect
from functools import wraps

# Set enviroment variable
os.environ["API_KEY"] = "GZZX52IAd0zxYaYnZOsw"

# Check for environment variable
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY is not set")


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def goodreads_review(isbn):
    """Look up reviews and ratings for  book."""
    
    # Contact API
    api_key = os.environ.get("API_KEY")
    response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
    if response.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    
    # Parse response
    try:
        data = response.json()
        return {
            "isbns": data["books"][0]["isbn"],
            "rate_count": data["books"][0]["ratings_count"],
            "rate_average": data["books"][0]["average_rating"]
        }
    except (KeyError, TypeError, ValueError):
        return None
    
def commaSeparator(value):
    """Format value for adding a comma for each group of three numbers, aka period."""
    return f"{value:,.0f}"