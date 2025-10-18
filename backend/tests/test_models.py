from app import app,db
from app import Book,User,BorrowRecord
from datetime import datetime

with app.app_context():

    # create Table
    db.drop_all()
    db.create_all()

    # Add test Users
    user1 = User(name="Alice2", email="alice2@example.com",phone="12345678902")
    user2 = User(name="Bob2", email="bob2@example.com", phone="12345678992")

    book1 = Book(title="Flask for Beginners2", author="John Doe2", isbn="123456789012322222222", genre="Programming2", publication_year=2023)
    book2 = Book(title="SQLAlchemy Deep Dive2", author="Jane Smith2", isbn="987654321098722", genre="Programming2", publication_year=2022)
    
    db.session.add_all([user1, user2, book1, book2])
    db.session.commit()

    # Borrow a Book
    borrow1 = BorrowRecord(user_id=user1.id,book_id=book1.id)
    db.session.add(borrow1)
    db.session.commit()

    # Query test
    borrows = BorrowRecord.query.all()
    for b in borrows:
        print(b.to_dict())