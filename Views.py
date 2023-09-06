import datetime
import re
from flask import Flask, request, jsonify
from sqlalchemy import exists, func
from components.BookDetails import Book
from components.Author import Author
from components.Profile import Profile
from components.Profile import CreditCards
from components.ShoppingCart import ShoppingCart
from components.ShoppingCart import BookShopping
from __main__ import db, app

"""
This file will contain all the routes with their functions. Make sure to add a
separator for your own section.
It is easier to maintain and check for conflicts if all the routes are in a
single file, make sure you are naming each function uniquely.
"""

# ******************** [1] Book Details ********************
@app.route("/admin/books", methods=["POST"])
def addBook():


@app.route("/admin/books", methods=["GET"])
def getBooks():

@app.route("/authors", methods=["GET"])
def getAuthors():


@app.route("/admin/createAuthor", methods=["POST"])
def createAuthor():

@app.route("/books/<ISBN>", methods=["GET"])

@app.route("/books/author/<AUTHOR>", methods=["GET"])
def getBooksByAuthor(AUTHOR):



# ******************** [1] Book Details ********************

# ******************** [2] Profile Management ********************
@app.route("/profile/createUser", methods=["POST"])
def addUser():


@app.route("/profile/getUsers", methods=["GET"])
def getUsers():

@app.route("/profile/<userName>", methods=["PUT"])
def updateUser(userName):

@app.route("/profile/<userName>/creditcards", methods=["POST"])
def addCards(userName):

@app.route("/profile/creditcards/<userName>", methods=["GET"])
def viewCards(userName):

# ******************** [2] Profile Management ********************


# ******************** [3] Book Browsing & Sorting *******************
@app.route("/books/genre/<GENRE>", methods=["GET"])
def getBooksByGenre(GENRE):

@app.route("/books/topSellers", methods=["GET"])
def getBooksByTopSellers():

@app.route("/books/rating/<RATING>", methods=["GET"])
def getBooksByRating(RATING):


@app.route("/books/limit/<LIMIT>", methods=["GET"])
def getBooksByLimit(LIMIT):

# ******************** [3] Book Browsing & Sorting *******************

# ******************** [4] Wishlist ************************






# ******************** [4] Wishlist ************************

# *********************[5] Shopping Cart *******************
@app.route("/admin/ShoppingCart", methods=["POST"])
def createShoppingCart():

@app.route("/admin/getShoppingCart", methods=["GET"])
def getShoppingCart():

@app.route("/admin/ShoppingCart/<userName>/<ISBN>", methods=["PUT"])
def addBooksToShoppingCart(userName, ISBN):

@app.route("/admin/ShoppingCart/<id>/<ISBN>", methods=["DELETE"])
def deleteBookFromShoppingCart(id, ISBN):

@app.route("/admin/ShoppingCart/<id>", methods=["GET"])
def getListFromShoppingCart(id):


# *********************[5] Shopping Cart *******************

# *********************[6] Rating **************************



# *********************[6] Rating **************************
