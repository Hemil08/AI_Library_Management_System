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
    
