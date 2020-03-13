# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 04:50:50 2020

@author: KennethJoel
"""


import os
import csv

from itertools import islice

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set enviroment variable
os.environ["DATABASE_URL"] = "postgres://zrhpostvgthsno:a148736d22595e7d028dd5fdba6ab602d10b8d7a45f2c5703fddb4c0630a1681@ec2-174-129-24-148.compute-1.amazonaws.com:5432/d1ho9el0dil0li"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL")) # database engine object from SQLAlchemy that manages connections to the
                                                  # DATABASE_URL is an environment variable that indicates where the database
db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with
                                                  # database are kept separate

# Open csv file
try:
    file = open("books.csv")
    reader = csv.reader(file)
except csv.Error:
    print("Unable to open the file.")

for isbn, title, author, year in islice(reader, 1, None): # loop gives each column a name and islice skip the first item(s).
    while len(isbn) < 10:
        isbn = "0" + isbn
    else:
        db.execute("UPDATE book SET isbn = :isbn WHERE title = :title AND author = :author", {"isbn" : isbn, "title" : title, "author" : author})
        print(f"Updated isbn book db to ISBN: {isbn}")
    
db.commit() #transactions are assumed, so close the transaction finished