#Ernesto Leiva
from marshmallow import fields
from __main__ import db, ma, app

class BookSchema(ma.Schema):
        class Meta:
            fields = (
                "id",
                "ISBN",
                "Name",
                "Description",
                "Price",
                "Author",
                "Genre",
                "Publisher",
                "YearPublished",
                "Sold",
                "Rating",
            )

# Product schema for single and multiple items
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Template class: [4] Book Details
class Book(db.Model):
    # Create DB fields
    id = db.Column(db.Integer, primary_key=True)
    ISBN = db.Column(db.Integer, unique=True)
    Name = db.Column(db.String(300), unique=True)
    Description = db.Column(db.String(2000))
    Price = db.Column(db.Float)
    Author = db.Column(db.String(300))
    Genre = db.Column(db.String(300))
    Publisher = db.Column(db.String(300))
    YearPublished = db.Column(db.Integer)
    Sold = db.Column(db.Integer)
    Rating = db.Column(db.Integer)

    def __init__(
        self, ISBN, Name, Desc, Price, Auth, Genre, Pub, Year, Sold, Rating
    ):  # noqa
        self.ISBN = ISBN
        self.Name = Name
        self.Description = Desc
        self.Price = Price
        self.Author = Auth
        self.Genre = Genre
        self.Publisher = Pub
        self.YearPublished = Year
        self.Sold = Sold
        self.Rating = Rating

    # @classmethod
    # def add_book(cls, isbn, name,description, genre, copies_sold, book_rating, price,publisher,author,year_published):
    #     with app.app_context():
    #         db.create_all()
    #         existing_book = cls.query.filter_by(isbn=isbn).first()
    #         if existing_book is None:
    #             new_book = cls(isbn=isbn, name=name,description=description, genre=genre, copies_sold=copies_sold, book_rating=book_rating, price=price,publisher=publisher,author=author,year_published=year_published)
    #             db.session.add(new_book)
    #             db.session.commit()
    #             return new_book
    #         else:
    #             return None  

    # @classmethod
    # def display_all_books(cls):
    #     with app.app_context():
    #         book_entries = cls.query.all()

    #         if book_entries:
    #          return books_schema.dumps(book_entries)
    #         else:
    #             return None
        