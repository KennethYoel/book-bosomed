# Project 1

Web Programming with Python and JavaScript

I've developed a book review website with 5 html pages, 3 js files, and 1 css file. Users will be able to register and then log in at another page, login.html. Then once logged into their account you'll arrive at the search.html page where one can search for a particular book by its isbn number, title, or author's name and then click on the book's title so to be taken to another page, book.html, showing more information on the book such as the book cover, a description, average rating from Goodreads and total ratings if any from Goodreads also. At the bottom of book.html users can add a review and a rating which it is stored into the db where it is added together to get the average and total ratings on my website.
Also created an API where users can make GET request to my website's /api/<isbn> route, returning a JSON response containing the book’s title,
author, publication date, ISBN number, review count, and average score from my db.

The files I've submitted contain's: scss file-with style.scss and config.scss. static file-where you'll find the typescript's for form-validation feather and a cookie-consent, an icon image file, and one css file. template file containing all of my html files.

Added a helpers file where the Goodreads API definiton resides and a format value definition. Also used untangle library for the xml data extracted from Goodreads API. Extrated the book description and the bookk cover image.
