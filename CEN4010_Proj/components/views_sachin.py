import datetime
import re
from flask import Flask, request, jsonify,make_response
from sqlalchemy import exists, func
from __main__ import db, app

from components.BookDetails import Book

"""
This file will contain all the routes with their functions. Make sure to add a
separator for your own section.
It is easier to maintain and check for conflicts if all the routes are in a
single file, make sure you are naming each function uniquely.
"""



# Get all books 
@app.route("/admin/books", methods=["GET"])
def getBooks():

    """Returns a json with all the books in the database"""
    
    books = Book.display_all_books()
    if books:
        return make_response(books, 200)
    else:
        return jsonify({"message": "No books found"}), 404


# ******************** [1] Book Browsing & Sorting (Sachin's API call) *******************


@app.route("/books/genre/<GENRE>", methods=["GET"])
def getBooksByGenre(GENRE):
    """Handles getting books by genre from the database"""

    books = Book.search_books_by_genre_JSON(GENRE)
    if books:
        return make_response(books, 200)
    else:
        return jsonify({"message": f"No books found for the genre {GENRE}"}), 404


@app.route("/books/topSellers", methods=["GET"])
def getBooksByTopSellers():
    """Handles getting books by top sellers from the database"""
    books = Book.search_top_ten_book_count_JSON()
    if books:
        return make_response(books, 200)
    else:
        return jsonify({"message": "No books found"}), 404
    

@app.route("/books/rating/<RATING>", methods=["GET"])
def getBooksByRating(RATING):
    """Handles getting books by a rating or higher from the database"""
    books = Book.search_books_by_book_rating_JSON(RATING)
    if books:
        return make_response(books, 200)
    else:
        return jsonify({"message": f"No books found for the rating {RATING}"}), 404
    

# Update discount prices by publisher
@app.route('/discount_books', methods=['PUT', 'PATCH'])
def discount_books_by_publisher():
    discount_percent = request.json.get('discount_percent')
    publisher = request.json.get('publisher')
    
    if not discount_percent or not publisher:
        return jsonify({"message": "Missing parameters"}), 400

    affected_rows = Book.update_discount_price_by_publisher(publisher,discount_percent)

    if affected_rows:
        return jsonify({"message": f"Discount applied to {affected_rows} books from {publisher}."}), 200
    else:
        return jsonify({"message": f"No books found from publisher {publisher}"}), 404

    
#Book.add_book(isbn=1089, name='The Lark', genre='Fiction', copies_sold=1000, book_rating=5, price=19.99,publisher="Barrons",author="Stine",year_published=2001,description="a stolid book")
#Book.add_book(isbn=2678, name='The White Pond', genre='Mystery', copies_sold=1005, book_rating=4, price=20.99,publisher="Kaplan",author="Steiner",year_published=2011,description="a nonfiction book")
#Book.add_book(isbn=3890, name='Death of Piano Man', genre='Fantasy', copies_sold=1078, book_rating=3, price=31.99,publisher="McGriffin",author="Henry",year_published=1998,description="a fiction book")
#Book.add_book(isbn=4789, name='Candy Dog', genre='Mystery', copies_sold=1178, book_rating=3, price=15.99,publisher="McGriffin",author="Thomas",year_published=1987,description="a solemn book")

# ******************** [1] Book Browsing & Sorting *******************

