#Sachin Konar

from marshmallow import fields
from __main__ import db, ma, app
from components.BookDetails import Book, books_schema

class BookSchema(ma.Schema):
    price = fields.Float()  
    class Meta:
    
        fields = ("id","isbn", "name","description", "genre", "copies_sold", "book_rating", "price","publisher","author","year_published")

#Initialize schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)  # To handle multiple Book objects
#db = SQLAlchemy(app)

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
            return Book.dumps(book_entries)
    else:
        return None

@classmethod
def list_books_by_book_name_JSON(cls, name):
    with app.app_context():
        book_entries = cls.query.filter_by(name=name).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None
@classmethod
def search_books_by_description_JSON(cls, description):
    with app.app_context():
        book_entries = cls.query.filter_by(description=description).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None
    
@classmethod
def search_top_ten_book_count_JSON(cls):
    with app.app_context():
        book_entries = cls.query.order_by(cls.copies_sold.desc()).limit(10).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
            return None


@classmethod
def search_books_by_genre_JSON(cls, genre):
    with app.app_context():
        book_entries = cls.query.filter_by(genre=genre).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None

@classmethod
def list_books_by_book_name_JSON(cls, name):
    with app.app_context():
        book_entries = cls.query.filter_by(name=name).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None

@classmethod
def search_books_by_description_JSON(cls, description):
    with app.app_context():
        book_entries = cls.query.filter_by(description=description).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None
    
@classmethod
def search_top_ten_book_count_JSON(cls):
    with app.app_context():
        book_entries = cls.query.order_by(cls.copies_sold.desc()).limit(10).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
            return None


@classmethod
def search_books_by_price_JSON(cls, price):
    with app.app_context():
        book_entries = cls.query.filter_by(price=price).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None


@classmethod
def search_books_by_book_rating_JSON(cls, book_rating):
    with app.app_context():
            book_entries = cls.query.filter(cls.book_rating >= book_rating).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None

@classmethod
def search_books_by_genre_JSON(cls, genre):
    with app.app_context():
        book_entries = cls.query.filter_by(genre=genre).all()

    if book_entries:
            return Book.dumps(book_entries)
    else:
        return None

@classmethod
def search_books_by_year_published_JSON(cls, year_published):
    with app.app_context():
        book_entries = cls.query.filter_by(year_published=year_published).all()

    if book_entries:
            return Book.dumps(book_entries)
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


