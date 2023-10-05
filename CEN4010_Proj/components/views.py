import datetime
import re
from flask import Flask, request, jsonify
from sqlalchemy import exists, func
from components.BookDetails import Book
from components.Author import Author
from components.Wishlist import Wishlist
from components.Profile import Profile
from components.Profile import CreditCards
from components.ShoppingCart import ShoppingCart
from components.ShoppingCart import BookShopping
from components.Rate import Rate
from __main__ import db, app


"""
This file will contain all the routes with their functions. Make sure to add a
separator for your own section.
It is easier to maintain and check for conflicts if all the routes are in a
single file, make sure you are naming each function uniquely.
"""


# ******************** [4] Book Details ********************
@app.route("/admin/books", methods=["POST"])
def addBook():
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
def getBooks():
    """Returns a json with all the books in the database"""
    # Query
    all_books = Book.query.all()

    result = Book.products_schema.dump(all_books)

    # Returns all the DB items as json
    return jsonify(result)


@app.route("/authors", methods=["GET"])
def getAuthors():
    """Returns a json with all the books in the database"""
    # Query
    all_authors = Author.query.all()

    result = Author.products_schema.dump(all_authors)

    # Returns all the DB items as json
    return jsonify(result)


@app.route("/admin/createAuthor", methods=["POST"])
def createAuthor():
    """Handles adding an author to the database"""
    # Fetch the POST request's fields
    FName = request.json["FirstName"]
    LName = request.json["LastName"]
    Biography = request.json["Biography"]
    Publisher = request.json["Publisher"]

    # Check if the author exists in the DB
    dupFName = db.session.query(exists().where(Author.FirstName == FName)).scalar()
    dupLName = db.session.query(exists().where(Author.LastName == LName)).scalar()

    if dupFName and dupLName:
        return jsonify("Author is already in the database.")

    # Create new book with fetched fields
    new_author = Author(FName, LName, Biography, Publisher)

    # Only add book if it's unique
    db.session.add(new_author)
    db.session.commit()

    # Return new_book as json
    return new_author.product_schema.jsonify(new_author)


@app.route("/books/<ISBN>", methods=["GET"])
def getBookByISBN(ISBN):
    """Returns the book requested by the specific ISBN route"""
    book = Book.query.get(ISBN)

    if book is None:
        return jsonify(None)

    return Book.product_schema.jsonify(book)


@app.route("/books/author/<AUTHOR>", methods=["GET"])
def getBooksByAuthor(AUTHOR):
    """Retrieve a list of books associated with an author"""
    # Get all books
    all_books = Book.query.all()

    # Append the book if its author was specified on the URL
    byAuthor = [
        Book.product_schema.dump(book)
        for book in all_books
        if book.Author.replace(" ", "") == AUTHOR  # noqa:
    ]

    # Check that the author has books in the database. If no books are found
    # by the author, return a json message saying so, and suggest authors.
    all_authors = Author.products_schema.dump(Author.query.all())
    if len(byAuthor) == 0:
        return jsonify(
            "No books written by this author in the database.",
            "Here is a list of authors recorded: ",
            all_authors,
        )

    # Returns all the DB items as json
    return jsonify(byAuthor)


# ******************** [4] Book Details ********************

# ******************** [2] Profile Management ********************
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

# ******************** [2] Profile Management ********************


# ******************** [1] Book Browsing & Sorting *******************
@app.route("/books/genre/<GENRE>", methods=["GET"])
def getBooksByGenre(GENRE):
    """Handles getting books by genre from the database"""

    # Get books by genre from db
    books = Book.query.filter(Book.Genre == GENRE)

    # Return books by genre as json
    results = Book.products_schema.dump(books)
    return jsonify(results)


@app.route("/books/topSellers", methods=["GET"])
def getBooksByTopSellers():
    """Handles getting books by top sellers from the database"""

    # Get books by top sellers from db
    books = Book.query.order_by(Book.Sold.desc()).limit(10)

    # Return books by top sellers as json
    results = Book.products_schema.dump(books)
    return jsonify(results)


@app.route("/books/rating/<RATING>", methods=["GET"])
def getBooksByRating(RATING):
    """Handles getting books by a rating or higher from the database"""

    # Get books by a specific rating or higher from db
    books = Book.query.filter(Book.Rating >= RATING)

    # Return books by a specific rating or higher as json
    results = Book.products_schema.dump(books)
    return jsonify(results)


@app.route("/books/limit/<LIMIT>", methods=["GET"])
def getBooksByLimit(LIMIT):
    """Returns a json with X books where X is an int in the database"""

    # Query
    all_books = Book.query.order_by(Book.Name.asc()).limit(LIMIT)

    result = Book.products_schema.dump(all_books)

    # Returns X books in the DB as json
    return jsonify(result)


# ******************** [1] Book Browsing & Sorting *******************

# ******************** [4] Wishlist ************************
@app.route("/wishList/createWishList", methods=["POST"])
def addWishlist():
    # Fetch the POST request's fields
    Title = request.json["Title"]
    Books = request.json["Books"]

    # Check if the wishlist title already exists
    duplicate = db.session.query(exists().where(Wishlist.Title == Title)).scalar()

    if duplicate:
        return jsonify("Wishlist tile already in use.")

    new_Wish = Wishlist(Title, Books)

    db.session.add(new_Wish)
    db.session.commit()

    return new_Wish.product_schema.jsonify(new_Wish)


@app.route("/wishList/<title>/<ISBN>", methods=["PUT"])
def addWishBook(title, ISBN):
    some_List = Wishlist.query.get(title)
    out = some_List.addBookToWish(ISBN)
    db.session.commit()

    return jsonify(out)


@app.route("/wishList/<title>", methods=["GET"])
def getBookInList(title):
    """Returns the books requested from a wishlist."""
    wish = Wishlist.query.filter_by(Title=title).first()

    if wish is None:
        return jsonify(None)

    return Wishlist.product_schema.jsonify(wish)


@app.route("/wishList/<title>/<ISBN>", methods=["DELETE"])
def removeBookInList(title, ISBN):

    some_List = Wishlist.query.get(title)
    out = some_List.removeBookInList(ISBN)
    db.session.commit()

    return jsonify(out)


# ******************** [4] Wishlist ************************

# *********************[6] Shopping Cart *******************
@app.route("/admin/ShoppingCart", methods=["POST"])
def createShoppingCart():
    """Handles adding a shopping cart to the database"""
    User = request.json["User"]

    # Create new book with fetched fields
    shopping_cart = ShoppingCart(User)

    # Only add book if it's unique
    db.session.add(shopping_cart)
    db.session.commit()

    # Return new_book as json
    return shopping_cart.product_schema.jsonify(shopping_cart)

@app.route("/admin/getShoppingCart", methods=["GET"])
def getShoppingCart():
    """Returns a json with all the profile in the database"""
    # Query
    all_ShoppingCart = ShoppingCart.query.all()

    result = ShoppingCart.products_schema.dump(all_ShoppingCart)

    # Returns all the DB items as json
    return jsonify(result)

@app.route("/admin/ShoppingCart/<userName>/<ISBN>", methods=["PUT"])
def addBooksToShoppingCart(userName, ISBN):
    # Attempt to find the user's shopping cart based on userName

    someOwner = ShoppingCart.query.filter_by(User=userName).first()

    exist = db.session.query(exists().where(Book.ISBN == ISBN)).scalar()

    if exist:
        aBook = Book.query.filter_by(ISBN=ISBN).first()
    else:
        return jsonify("ERROR: Book does not exist")

    temp = BookShopping(aBook)
    temp.ownerId = someOwner.id
    temp.bookId = aBook.id

    db.session.add(temp)
    db.session.commit()

    return temp.product_schema.jsonify(temp)

@app.route("/admin/ShoppingCart/<id>/<ISBN>", methods=["DELETE"])
def deleteBookFromShoppingCart(id, ISBN):
    result = " "

    entry_to_delete = db.session.query(BookShopping).filter_by(ownerId=id, bookId=ISBN).first()
    if entry_to_delete:
        result = {
            "id": entry_to_delete.id,
            "ownerId": entry_to_delete.ownerId,
            "bookId": entry_to_delete.bookId,
            # Add other attributes as needed
        }
        db.session.delete(entry_to_delete)
        db.session.commit()
    else:
        return jsonify("ERROR: Book does not exist")

    # Returns all the DB items as json
    return jsonify(result)

@app.route("/admin/ShoppingCart/<id>", methods=["GET"])
def getListFromShoppingCart(id):
    # Query the database to retrieve entries with ownerId equal to 5
    all_profile = BookShopping.query.filter(BookShopping.ownerId == id).all()

    result = BookShopping.products_schema.dump(all_profile)

    # Returns all the DB items as json
    return jsonify(result)


# *********************[6] Shopping Cart *******************

# *********************[7] Rating and comments *******************

@book_bp.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_data = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
    return jsonify(book_data)

@book_bp.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_data = {'id': book.id, 'title': book.title, 'author': book.author}
    return jsonify(book_data)

@book_bp.route('/book/<int:book_id>/ratings', methods=['GET'])
def get_book_ratings(book_id):
    ratings = Rating.query.filter_by(book_id=book_id).all()
    rating_data = [{'id': rating.id, 'value': rating.value, 'user_id': rating.user_id, 'timestamp': rating.timestamp} for rating in ratings]
    return jsonify(rating_data)

@book_bp.route('/book/<int:book_id>/comments', methods=['GET'])
def get_book_comments(book_id):
    comments = Comment.query.filter_by(book_id=book_id).all()
    comment_data = [{'id': comment.id, 'text': comment.text, 'user_id': comment.user_id, 'timestamp': comment.timestamp} for comment in comments]
    return jsonify(comment_data)

@book_bp.route('/book/<int:book_id>/average_rating', methods=['GET'])
def get_average_rating(book_id):
    average_rating = Rating.query.filter_by(book_id=book_id).with_entities(func.avg(Rating.value)).scalar()
    return jsonify({'average_rating': average_rating})

@book_bp.route('/book/<int:book_id>/rate', methods=['POST'])
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

@book_bp.route('/book/<int:book_id>/comment', methods=['POST'])
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


# *********************[7] Rating and comments *******************