#Ernesto Leiva
from __main__ import db, ma, app

class Book(db.Model):

    class ProductSchema(ma.Schema):
        
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


    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)

    def __init__(
        self, ISBN, Name, Desc, Price, Auth, Genre, Pub, Year, Sold, Rating
    ):  
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

class Author(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    Biography = db.Column(db.Text)
    Publisher = db.Column(db.String(100))


    def __init__(self, FirstName, LastName, Biography, Publisher):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Biography = Biography
        self.Publisher = Publisher

    class AuthorSchema(ma.Schema):
        
        class Meta:
            fields = (
                "id",
                "FirstName",
                "LastName",
                "Biography",
                "Publisher")

        books = ma.Nested(Book.ProductSchema, many=True)

    author_schema = AuthorSchema()
    authors_schema = AuthorSchema(many=True)