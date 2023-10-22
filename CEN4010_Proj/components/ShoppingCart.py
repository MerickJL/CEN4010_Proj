#Maverick Lenon
from __main__ import db, ma
from components.BookDetails import Book

class ShoppingCart(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = (
                "id",
                "User",
            )

    # Create DB fields
    id = db.Column(db.Integer, primary_key=True)
    User = db.Column(db.String(300), unique=True)
    books = db.relationship("BookShopping", backref="owner")
    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, User):
        self.User = User

    def addBookToShoppingCart(self, ISBN):
        self.Books = self.Books + ISBN
        return "Book " + Book.query.get(int(ISBN)).Name + " has been added"

    def deleteBookFromShoppingCart(self, ISBN):
        newListAfterDeletion = ""
        for book in self.Books:
            if book != ISBN:
                newListAfterDeletion = newListAfterDeletion + book
        if newListAfterDeletion == self.Books:
            return "Book to be deleted was not found in shopping cart"
        else:
            self.Books = newListAfterDeletion
            return "Book " + Book.query.get(int(ISBN)).Name + " has been deleted"

class BookShopping(db.Model):
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("bookId", "ownerId")

    id = db.Column(db.Integer, primary_key=True)
    bookId = db.Column(db.Integer)
    ownerId = db.Column(db.Integer, db.ForeignKey("shopping_cart.id"))

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, books):
        self.books = books