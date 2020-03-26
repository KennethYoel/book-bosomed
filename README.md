# Project 1

Web Programming with Python and JavaScript

What we have here is a book review website where users will be able to register at the home page, index.html, and then routed to another page, login.html, allowing the user to log in. Then once logged into their account the user will be routed to the search.html page where one can search for a particular book by its isbn number, title, or author's name. Then click on the book's title so to be taken to another page, book.html, showing more information on the book such as the book cover, a description, average rating and total ratings if any from Goodreads. At the bottom of book.html users can add a review and a rating which it is stored into the db where it is added together to get the average and total ratings on my website.
Also created an API where users can make GET request to my website's /api/<isbn> route, returning a JSON response containing the book’s title,
author, publication date, ISBN number, review count, and average score from my db.

The files I've submitted contain's: scss file-with style.scss and config.scss. static file-where you'll find the typescript's for form-validation feather and a cookie-consent, an icon image file, a svg img file, and one css file. And template file-containing all six html files.

Added a helpers file where the Goodreads API function resides and a format value function. Also used untangle library for getting the XML data from the Goodreads API, extracting the book description and the book cover image.
