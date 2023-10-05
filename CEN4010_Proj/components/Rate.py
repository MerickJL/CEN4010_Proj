#Grecia Lara
# app/models.py
from datetime import datetime
from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    ratings = db.relationship('Rating', backref='book', lazy=True)
    comments = db.relationship('Comment', backref='book', lazy=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


 #app/routes.py
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app import db
from app.models import Book, Rating, Comment

book_bp = Blueprint('book_bp', __name__)

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

