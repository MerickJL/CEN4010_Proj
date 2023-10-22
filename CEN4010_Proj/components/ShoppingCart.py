#Maverick Lenon
from __main__ import db, ma
from components.Browsing_and_sorting import Book

# Association table for many-to-many relationship between ShoppingCart and Book
shoppingcart_books_association = db.Table('shoppingcart_books',
    db.Column('shoppingcart_id', db.Integer, db.ForeignKey('shoppingcart.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'))
)

class ShoppingCart(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("id", "User", "books")

    # Create DB fields
    id = db.Column(db.Integer, primary_key=True)
    User = db.Column(db.String(300), unique=True, nullable=False)
    books = db.relationship('Book', secondary=shoppingcart_books_association, lazy='subquery',
        backref=db.backref('shoppingcarts', lazy=True))

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, User, books=None):
        self.User = User
        if books:
            self.books = books

    def add_book(self, ISBN):
        book = Book.query.get(ISBN)
        if not book:
            return f"Book with ISBN {ISBN} not found"
        if book not in self.books:
            self.books.append(book)
            return f"Book {book.name} has been added to shopping cart"
        return f"Book {book.name} is already in the shopping cart"

    def remove_book(self, ISBN):
        book = Book.query.get(ISBN)
        if not book:
            return f"Book with ISBN {ISBN} not found"
        if book in self.books:
            self.books.remove(book)
            return f"Book {book.name} has been removed from shopping cart"
        return f"Book {book.name} is not in the shopping cart"
