#Grecia Lara
from __main__ import db, ma, app

class Rate(db.Model):
    # Schema
    class ProductSchema(ma.Schema):
        class Meta:
            fields = ("isbn", "username", "rating", "comment", "time")

    # Create DB fields
    isbn = db.Column(db.Integer)
    username = db.Column(db.String(300), primary_key=True)
    rating = db.Column(db.Integer)
    comment = db.Column(db.String(300))
    time = db.Column(db.String(300))

    # Product schema for single and multiple items
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(self, isbn, username, rating, comment, time):
        self.isbn = isbn
        self.username = username
        self.rating = rating
        self.comment = comment
        self.time = time

# class Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)

