from __main__ import db, ma
from components.BookDetails import Book

wishlist_books_association = db.Table('wishlist_books',
    db.Column('wishlist_id', db.Integer, db.ForeignKey('wishlist.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)
class Wishlist(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
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

    def add_book(self, ISBN):
        book = Book.query.get(ISBN)
        if not book:
            return f"Book with ISBN {ISBN} not found"
        if book not in self.books:
            self.books.append(book)
            return f"Book {book.name} has been added to wishlist"
        return f"Book {book.name} is already in the wishlist"

    def remove_book(self, ISBN):
        book = Book.query.get(ISBN)
        if not book:
            return f"Book with ISBN {ISBN} not found"
        if book in self.books:
            self.books.remove(book)
            return f"Book {book.name} has been removed from wishlist"
        return f"Book {book.name} is not in the wishlist"
