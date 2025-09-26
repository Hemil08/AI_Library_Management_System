from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Databases Models
class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    author = db.Column(db.String(20),unique=True,nullable=False)
    isbn = db.Column(db.String(20),unique=True,nullable=False)
    genre = db.Column(db.String(100))
    publication_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    available = db.Column(db.Boolean,default=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'genre': self.genre,
            'publication_year': self.publication_year,
            'description': self.description,
            'available': self.available,
            'created_at': self.created_at.isoformat()
        }
    
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    def to_dict(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat()
        }
    
class BorrowRecord(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    book_id = db.Column(db.Integer,db.ForeignKey('book.id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    borrow_date = db.Column(db.DateTime,default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean,default=False)

    book = db.relationship('Book',backref='borrow_records')
    user = db.relationship('User',backref='borrow_records')

    def to_dict(self):
        return {
            'id':self.id,
            'book_id':self.book_id,
            'user_id':self.user_id,
            'borrow_date':self.borrow_date.isoformat(),
            'return_date':self.return_date.isoformat() if self.return_date else None,
            'returned':self.returned,
            'book':self.book.to_dict(),
            'user':self.user.to_dict()
        }
    

# API Routes

@app.route('/api/books',method=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

@app.route('/api/books',method=['POST'])
def add_book():
    data = request.get_json()

    # Generate AI description if not provided
    

    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        genre=data.get('genre'),
        publication_year = data.get('publication_year'),
        description = data['description']
    )

    try:
        db.session.add(book)
        db.session.commit()
        return jsonify(book.to_dict()),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),400
    
@app.route('/api/books/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    book.title = data.get('title',book.title)
    book.author = data.get('author',book.author)
    book.isbn = data.get('isbn',book.isbn)
    book.genre = data.get('genre',book.genre)
    book.publication_year = data.get('publication_year',book.publication_year)
    book.description = data.get('description',book.description)
    book.available = data.get('available',book.available)

    try:
        db.session.commit()
        return jsonify(book.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),400

@app.route('/api/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        return '',204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),400
    
@app.route('/api/search',methods=['POST'])
def search_books():
    data = request.get_json()
    query = data.get('query','')

    all_books = Book.query.all()

    if not query:
        return jsonify([book.to_dict() for book in all_books])
    
    # Use AI for smart search


    # Get books in order of AI ranking
    


    # return jsonify([book.to_dict() for book in ordered_books
    

# @app.route('/api/recommendations', methods=['POST'])
# def get_recommendations():
#     data = request.get_json()
    
@app.route('/api/users',methods='POST')
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users',methods=['POST'])
def add_user():
    data = request.get_json()

    user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone')
    )

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()),201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),400
    
@app.route('/api/borrow',methods=['POST'])
def borrow_book():
    data = request.get_json()
    book_id = data['book_id']
    user_id = data['user_id']

    book = Book.query.get_or_404(book_id)
    user = User.query.get_or_404(user_id)

    if not book.available:
        return jsonify({'error':'Book is not available'}),400
    
    borrow_record = BorrowRecord(book_id=book_id,user_id=user_id)
    book.available = False

    try:
        db.session.add(borrow_record)
        db.session.commit()
        return jsonify({'error':str(e)}),400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),400
    
@app.route('/api/return',methods=['POST'])
def return_book():
    data = request.get_json()
    record_id = data['record_id']

    record = BorrowRecord.query.get_or_404(record_id)

    if record.returned:
        return jsonify({'error':'Book already returned'}),400
    
    record.returned = True
    record.return_date = datetime.utcnow()
    record.book.available = True
    
    try:
        db.session.commit()
        return jsonify(record.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),400
    
@app.route('/api/borrow-records',methods=['GET'])
def get_borrow_records():
    records = BorrowRecord.query.all()
    return jsonify([record.to_dict() for record in records])

@app.route('/api/stats',methods=['GET'])
def get_stats():
    total_books = Book.query.count()
    available_books = Book.query.filter_by(available=True).count()
    borrowed_books = Book.query.filter_by(available=False).count()
    total_users = User.query.count()
    active_borrows = BorrowRecord.query.filter_by(returned=False).count()

    return jsonify({
        'total_books':total_books,
        'available_books':available_books,
        'borrowed_books':borrowed_books,
        'total_users':total_users,
        'active_borrows':active_borrows
    })

