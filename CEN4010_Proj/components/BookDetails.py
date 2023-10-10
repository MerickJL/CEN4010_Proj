#Sachin Konar
import sys
print(sys.path)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from __main__ import db, ma, app

# Flask app
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'  # SQLite database

# Initialize Marshmallow
#ma = Marshmallow(app)



class BookSchema(ma.Schema):
    price = fields.Float()  
    class Meta:
        
        fields = ("id","isbn", "name","description", "genre", "copies_sold", "book_rating", "price","publisher","author","year_published")

# Initialize schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)  # To handle multiple Book objects
#db = SQLAlchemy(app)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    isbn = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=False, nullable=False)
    genre = db.Column(db.String(80), unique=False, nullable=False)
    copies_sold = db.Column(db.Integer, unique=False, nullable=False)
    book_rating = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Numeric(6, 2), unique=False, nullable=False)
    publisher = db.Column(db.String(80), unique=False, nullable=False)
    author = db.Column(db.String(80), unique=False, nullable=False)
    year_published = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, isbn, name,description, genre, copies_sold, book_rating, price,publisher,author,year_published):
        self.isbn = isbn
        self.name = name
        self.description=description
        self.genre = genre
        self.copies_sold = copies_sold
        self.book_rating = book_rating
        self.price = price
        self.publisher = publisher
        self.author = author
        self.year_published = year_published
        

    #tested
    @classmethod
    def update_discount_book(cls, publisher,discount_percent):
        with app.app_context():
             affected_rows = Book.query.filter_by(publisher=publisher).update({
                'price': Book.price - (Book.price * discount_percent / 100)
        })
        db.session.commit()
        if affected_rows:
            return affected_rows
        else:
            return None



    @classmethod
    def search_books_by_genre_JSON(cls, genre):
        with app.app_context():
            book_entries = cls.query.filter_by(genre=genre).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None
    
    @classmethod
    def list_books_by_book_name_JSON(cls, name):
        with app.app_context():
            book_entries = cls.query.filter_by(name=name).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None
    @classmethod
    def search_books_by_description_JSON(cls, description):
        with app.app_context():
            book_entries = cls.query.filter_by(description=description).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None
        
    @classmethod
    def search_top_ten_book_count_JSON(cls):
        with app.app_context():
            book_entries = cls.query.order_by(cls.copies_sold.desc()).limit(10).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
             return None
   
    
    @classmethod
    def searchBooksByPriceJSON(cls, price):
        with app.app_context():
            book_entries = cls.query.filter_by(price=price).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None

    
    @classmethod
    def search_books_by_book_rating_JSON(cls, book_rating):
        with app.app_context():
             book_entries = cls.query.filter(cls.book_rating >= book_rating).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None
    
    @classmethod
    def search_books_by_genre_JSON(cls, genre):
        with app.app_context():
            book_entries = cls.query.filter_by(genre=genre).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None
   
    @classmethod
    def search_books_by_year_published_JSON(cls, year_published):
        with app.app_context():
            book_entries = cls.query.filter_by(year_published=year_published).all()

        if book_entries:
             return books_schema.dumps(book_entries)
        else:
            return None
        
    @classmethod
    def add_book(cls, isbn, name,description, genre, copies_sold, book_rating, price,publisher,author,year_published):
        with app.app_context():
            db.create_all()
            existing_book = cls.query.filter_by(isbn=isbn).first()
            if existing_book is None:
                new_book = cls(isbn=isbn, name=name,description=description, genre=genre, copies_sold=copies_sold, book_rating=book_rating, price=price,publisher=publisher,author=author,year_published=year_published)
                db.session.add(new_book)
                db.session.commit()
                return new_book
            else:
                return None  

    @classmethod
    def display_all_books(cls):
        with app.app_context():
            book_entries = cls.query.all()

            if book_entries:
             return books_schema.dumps(book_entries)
            else:
                return None
    
    @classmethod
    def update_discount_price_by_publisher(cls,publisher,discount_percent):
        with app.app_context():
                        
            books_to_update = cls.query.filter_by(publisher=publisher).all()

            if not books_to_update:
                return None

            # Update each book's price
            for book in books_to_update:
                new_price = book.price - (book.price * discount_percent / 100)
                book.price = new_price

            db.session.commit()        
        
        return len(books_to_update)





#Book.display_all_books()
