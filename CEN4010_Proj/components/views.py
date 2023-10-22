import datetime
import re
from flask import Flask, request, jsonify, make_response
from sqlalchemy import exists, func
from components.BookDetails import Book
from components.Wishlist import Wishlist
from components.Profile import Profile, CreditCards
from components.ShoppingCart import ShoppingCart
from components.ShoppingCart import BookShopping
from components.Rate import Rating, Comment
from __main__ import db, app

# ******************** [1] Book Details ********************
@app.route("/admin/books", methods=["POST"])
def add_Book():
    """Handles adding a book to the database"""
    # Fetch the POST request's fields
    ISBN = request.json["ISBN"]
    Name = request.json["Name"]
    Description = request.json["Description"]
    Price = request.json["Price"]
    Author = request.json["Author"]
    Genre = request.json["Genre"]
    Publisher = request.json["Publisher"]
    YearPublished = request.json["YearPublished"]
    Sold = request.json["Sold"]
    Rating = request.json["Rating"]

    # Check if the book exists in the DB
    duplicate = db.session.query(exists().where(Book.Name == Name)).scalar()

    if duplicate:
        return jsonify("Book name is already in the database")

    # Create new book with fetched fields
    new_book = Book(
        ISBN, Name, Description, Price, Author, Genre, Publisher, YearPublished, Sold, Rating
    )  # noqa

    # Only add book if it's unique
    db.session.add(new_book)
    db.session.commit()

    # Return new_book as json
    return new_book.product_schema.jsonify(new_book)

@app.route("/admin/books", methods=["GET"])
def display_all_books():
    # Query
    all_books = Book.query.all()

    result = Book.products_schema.dump(all_books)

    # Returns all the DB items as json
    return jsonify(result)

# ******************** [1] Book Details ********************

# ******************** [2] Book Sorting********************
@app.route("/books/<ISBN>", methods=["GET"])
def getBookByISBN(ISBN):
    """Returns the book requested by the specific ISBN route"""
    book = Book.query.get(ISBN)

    if book is None:
        return jsonify(None)

    return Book.product_schema.jsonify(book)
     
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
    
# @app.route("/books/genre/<GENRE>", methods=["GET"])
# def getBooksByGenre(GENRE):
#     """Handles getting books by genre from the database"""

#     # Get books by genre from db
#     books = Book.query.filter(Book.Genre == GENRE)

#     # Return books by genre as json
#     results = Book.products_schema.dump(books)
#     return jsonify(results)

# @app.route("/books/topSellers", methods=["GET"])
# def getBooksByTopSellers():
#     """Handles getting books by top sellers from the database"""

#     # Get books by top sellers from db
#     books = Book.query.order_by(Book.Sold.desc()).limit(10)

#     # Return books by top sellers as json
#     results = Book.products_schema.dump(books)
#     return jsonify(results)

# @app.route("/books/rating/<RATING>", methods=["GET"])
# def getBooksByRating(RATING):
#     """Handles getting books by a rating or higher from the database"""

#     # Get books by a specific rating or higher from db
#     books = Book.query.filter(Book.Rating >= RATING)

#     # Return books by a specific rating or higher as json
#     results = Book.products_schema.dump(books)
#     return jsonify(results)

# @app.route("/books/limit/<LIMIT>", methods=["GET"])
# def getBooksByLimit(LIMIT):
#     """Returns a json with X books where X is an int in the database"""

#     # Query
#     all_books = Book.query.order_by(Book.Name.asc()).limit(LIMIT)

#     result = Book.products_schema.dump(all_books)

#     # Returns X books in the DB as json
#     return jsonify(result)

    
#Book.add_book(isbn=1089, name='The Lark', genre='Fiction', copies_sold=1000, book_rating=5, price=19.99,publisher="Barrons",author="Stine",year_published=2001,description="a stolid book")
#Book.add_book(isbn=2678, name='The White Pond', genre='Mystery', copies_sold=1005, book_rating=4, price=20.99,publisher="Kaplan",author="Steiner",year_published=2011,description="a nonfiction book")
#Book.add_book(isbn=3890, name='Death of Piano Man', genre='Fantasy', copies_sold=1078, book_rating=3, price=31.99,publisher="McGriffin",author="Henry",year_published=1998,description="a fiction book")
#Book.add_book(isbn=4789, name='Candy Dog', genre='Mystery', copies_sold=1178, book_rating=3, price=15.99,publisher="McGriffin",author="Thomas",year_published=1987,description="a solemn book")

# ******************** [2] Book Sorting ********************

# ******************** [3] Profile Management ********************
@app.route("/profile/createUser", methods=["POST"])
def addUser():
    """Handles creating a user profile in the databse"""

    # pattern used from username(email) input
    regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

    # Fetch the POST request's fields
    UserName = request.json["UserName"]
    Password = request.json["Password"]
    Name = request.json["Name"]
    HomeAddress = request.json["HomeAddress"]

    # check if username is valid
    if (re.search(regex, UserName)) == None:
        return jsonify("Invalid username")

    # Check if the username already exists in the DB
    duplicate = db.session.query(exists().where(Profile.UserName == UserName)).scalar()

    if duplicate:
        return jsonify("Username already in use")

    # Create new user with fetched fields
    new_user = Profile(UserName, Password, Name, HomeAddress)

    # Only add user if it's unique
    db.session.add(new_user)
    db.session.commit()

    # Return new_user as json
    return new_user.product_schema.jsonify(new_user)

@app.route("/profile/getUsers", methods=["GET"])
def getUsers():
    """Returns a json with all the profile in the database"""
    # Query
    all_profile = Profile.query.all()

    result = Profile.products_schema.dump(all_profile)

    # Returns all the DB items as json
    return jsonify(result)

@app.route("/profile/<userName>", methods=["GET"])
def getUserByUsername(userName):
    """Returns the searched user requested using the username"""
    user = Profile.query.filter_by(UserName=userName).first()

    # check if user exists
    if user is None:
        return jsonify(None)

    return Profile.product_schema.jsonify(user)

@app.route("/profile/<userName>", methods=["PUT"])
def updateUser(userName):
    user = Profile.query.filter_by(UserName=userName).first()

    # check if user exists
    if user is None:
        return jsonify(None)

    # Fetch the PUT request's fields
    Password = request.json["Password"]
    Name = request.json["Name"]
    HomeAddress = request.json["HomeAddress"]

    user.Password = Password
    user.Name = Name
    user.HomeAddress = HomeAddress

    db.session.commit()

    # Update user fields
    return user.product_schema.jsonify(user)

@app.route("/profile/<userName>/creditcards", methods=["POST"])
def addCards(userName):
    someOwner = Profile.query.filter_by(UserName=userName).first()

    # check if user exists
    if someOwner is None:
        return jsonify(None)

    cardNumber = request.json["cardNumber"]
    expirationDate = request.json["expirationDate"]
    cvs = request.json["cvs"]

    duplicate = db.session.query(
        exists().where(CreditCards.cardNumber == cardNumber)
    ).scalar()

    # check to see if card already in database
    if duplicate:
        return jsonify("card already in use")

    newCard = CreditCards(cardNumber, expirationDate, cvs)
    newCard.ownerId = someOwner.id

    db.session.add(newCard)
    db.session.commit()

    return newCard.product_schema.jsonify(newCard)

@app.route("/profile/creditcards/<userName>", methods=["GET"])
def viewCards(userName):
    someOwner = Profile.query.filter_by(UserName = userName).first()
    
    # check if user exists
    if someOwner is None:
        return jsonify("user does not exist")

    all_cards = CreditCards.query.filter_by(ownerId = someOwner.id)

    result = CreditCards.products_schema.dump(all_cards)

    # Returns all the DB items as json
    return jsonify(result)

# ******************** [3] Profile Management ********************

# ******************** [4] Wishlist ************************
@app.route("/wishList", methods=["POST"])
def create_wishlist():
    # Fetch the POST request's fields
    title = request.json["title"]
    
    # Check if the wishlist title already exists
    existing_wishlist = Wishlist.query.filter_by(title=title).first()
    if existing_wishlist:
        return jsonify("Wishlist title already in use."), 400

    new_wishlist = Wishlist(title)
    db.session.add(new_wishlist)
    db.session.commit()

    return new_wishlist.product_schema.jsonify(new_wishlist), 201

@app.route("/wishList/<title>/books/<ISBN>", methods=["PUT"])
def add_book_to_wishlist(title, ISBN):
    wishlist = Wishlist.query.filter_by(title=title).first()
    if not wishlist:
        return jsonify(f"Wishlist {title} not found"), 404

    message = wishlist.add_book(ISBN)
    db.session.commit()

    return jsonify(message)

@app.route("/wishList/<title>", methods=["GET"])
def get_books_in_wishlist(title):
    wishlist = Wishlist.query.filter_by(title=title).first()
    if not wishlist:
        return jsonify(f"Wishlist {title} not found"), 404

    return Wishlist.product_schema.jsonify(wishlist)

@app.route("/wishList/<title>/books/<ISBN>", methods=["DELETE"])
def remove_book_from_wishlist(title, ISBN):
    wishlist = Wishlist.query.filter_by(title=title).first()
    if not wishlist:
        return jsonify(f"Wishlist {title} not found"), 404

    message = wishlist.remove_book(ISBN)
    db.session.commit()

    return jsonify(message)

# ******************** [4] Wishlist ************************

# *********************[5] Shopping Cart *******************
@app.route("/admin/ShoppingCart", methods=["POST"])
def createShoppingCart():
    """Handles adding a shopping cart to the database"""
    User = request.json["User"]

    # Check if the shopping cart for the user already exists
    existing_cart = ShoppingCart.query.filter_by(User=User).first()
    if existing_cart:
        return jsonify("Shopping cart for this user already exists."), 400

    # Create new shopping cart with fetched fields
    shopping_cart = ShoppingCart(User)
    db.session.add(shopping_cart)
    db.session.commit()

    return shopping_cart.product_schema.jsonify(shopping_cart), 201

@app.route("/admin/getShoppingCart", methods=["GET"])
def getAllShoppingCarts():
    # Returns a json with all the shopping carts in the database
    all_ShoppingCart = ShoppingCart.query.all()
    result = ShoppingCart.products_schema.dump(all_ShoppingCart)
    return jsonify(result)

@app.route("/admin/ShoppingCart/<userName>/books/<ISBN>", methods=["PUT"])
def addBooksToShoppingCart(userName, ISBN):
    shopping_cart = ShoppingCart.query.filter_by(User=userName).first()
    if not shopping_cart:
        return jsonify(f"Shopping cart for user {userName} not found"), 404

    book = Book.query.get(ISBN)
    if not book:
        return jsonify(f"Book with ISBN {ISBN} not found"), 404

    if book in shopping_cart.books:
        return jsonify(f"Book with ISBN {ISBN} is already in the shopping cart"), 400

    shopping_cart.books.append(book)
    db.session.commit()

    return jsonify(f"Book with ISBN {ISBN} added to shopping cart"), 200

@app.route("/admin/ShoppingCart/<userName>/books/<ISBN>", methods=["DELETE"])
def removeBookFromShoppingCart(userName, ISBN):
    shopping_cart = ShoppingCart.query.filter_by(User=userName).first()
    if not shopping_cart:
        return jsonify(f"Shopping cart for user {userName} not found"), 404

    book = Book.query.get(ISBN)
    if not book:
        return jsonify(f"Book with ISBN {ISBN} not found"), 404

    if book not in shopping_cart.books:
        return jsonify(f"Book with ISBN {ISBN} is not in the shopping cart"), 400

    shopping_cart.books.remove(book)
    db.session.commit()

    return jsonify(f"Book with ISBN {ISBN} removed from shopping cart"), 200

@app.route("/admin/ShoppingCart/<userName>", methods=["GET"])
def getListFromShoppingCart(userName):
    shopping_cart = ShoppingCart.query.filter_by(User=userName).first()
    if not shopping_cart:
        return jsonify(f"Shopping cart for user {userName} not found"), 404

    return ShoppingCart.product_schema.jsonify(shopping_cart)

# *********************[5] Shopping Cart *******************

# *********************[6] Rating and comments *******************
@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_data = {'id': book.id, 'title': book.title, 'author': book.author}
    return jsonify(book_data)

@app.route('/book/<int:book_id>/ratings', methods=['GET'])
def get_book_ratings(book_id):
    ratings = Rating.query.filter_by(book_id=book_id).all()
    rating_data = [{'id': rating.id, 'value': rating.value, 'user_id': rating.user_id, 'timestamp': rating.timestamp} for rating in ratings]
    return jsonify(rating_data)

@app.route('/book/<int:book_id>/comments', methods=['GET'])
def get_book_comments(book_id):
    comments = Comment.query.filter_by(book_id=book_id).all()
    comment_data = [{'id': comment.id, 'text': comment.text, 'user_id': comment.user_id, 'timestamp': comment.timestamp} for comment in comments]
    return jsonify(comment_data)

@app.route('/book/<int:book_id>/average_rating', methods=['GET'])
def get_average_rating(book_id):
    average_rating = Rating.query.filter_by(book_id=book_id).with_entities(func.avg(Rating.value)).scalar()
    return jsonify({'average_rating': average_rating})

@app.route('/book/<int:book_id>/rate', methods=['POST'])
def rate_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if 'value' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid request. Please provide value and user_id.'}), 400

    rating_value = int(data['value'])
    user_id = int(data['user_id'])

    if 1 <= rating_value <= 5:
        rating = Rating(value=rating_value, book=book, user_id=user_id)
        db.session.add(rating)
        db.session.commit()
        return jsonify({'message': 'Rating submitted successfully!'}), 201
    else:
        return jsonify({'error': 'Invalid rating value. Please choose a rating between 1 and 5.'}), 400

@app.route('/book/<int:book_id>/comment', methods=['POST'])
def comment_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if 'text' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid request. Please provide text and user_id.'}), 400

    comment_text = data['text']
    user_id = int(data['user_id'])

    if comment_text:
        comment = Comment(text=comment_text, book=book, user_id=user_id)
        db.session.add(comment)
        db.session.commit()
        return jsonify({'message': 'Comment submitted successfully!'}), 201
    else:
        return jsonify({'error': 'Please enter a comment.'}), 400

# *********************[6] Rating and comments *******************
