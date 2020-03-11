# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 16:21:10 2020

@author: KennethJoel
"""


import requests
import os

# Set enviroment variable
os.environ["API_KEY"] = "GZZX52IAd0zxYaYnZOsw"

# Check for environment variable
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY is not set")


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
    
def comma(value):
    """Format value for comma placement."""
    return f"{value:,.0f}"