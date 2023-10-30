#Ernesto Leiva
from __main__ import db, ma
from components.BookDetails import Book

wishlist_books_association = db.Table('wishlist_books',
    db.Column('wishlist_id', db.Integer, db.ForeignKey('wishlist.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)
class Wishlist(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        books = ma.Nested(Book.ProductSchema, many=True)
        class Meta:
            fields = ("id", "title", "books")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), unique=True, nullable=False)
    books = db.relationship('Book', secondary=wishlist_books_association, lazy='subquery',
        backref=db.backref('wishlists', lazy=True))

    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, title, books=None):
        self.title = title
        if books:
            self.books = books

    def check_for_book(self, ISBN):
        book = Book.query.filter_by(ISBN=ISBN).first()

        if not book:
            return f"Book with ISBN {ISBN} not found", book
        else:
            return None, book

    def add_book(self, ISBN):
        message, book = self.check_for_book(ISBN)
        if message:
            return message, 404
        if book not in self.books:
            self.books.append(book)
            return f"Book '{book.Name}' has been added to wishlist", 200
        return f"Book '{book.Name}' is already in the wishlist", 400

    def remove_book(self, ISBN):
        message, book = self.check_for_book(ISBN)
        if message:
            return message, 404
        if book in self.books:
            self.books.remove(book)
            return f"Book '{book.Name}' has been removed from wishlist", 200
        return f"Book '{book.Name}' is not in the wishlist", 404
