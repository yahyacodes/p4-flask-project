from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model,SerializerMixin):

    serialize_only = ('username', 'email')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

class Profile(db.Model,SerializerMixin):

    serialize_only = ('firstname', 'lastname', 'user')

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='profile', uselist=False)

class Book(db.Model,SerializerMixin):

    serialize_only = ('id', 'title', 'description', 'author.authorname')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('Author', backref='books')
    user = db.relationship('User', backref='books')
    categories = db.relationship('BookCategory', secondary='book_category_association', back_populates='book')

class Borrow(db.Model,SerializerMixin):

    serialize_only = ('date', 'return_date', 'book.title', 'book.description', 'book.author', 'user.username')
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    book = db.relationship('Book', backref='borrows')
    user = db.relationship('User', backref='borrows')

class BookCategory(db.Model,SerializerMixin):

    serialize_only = ('categoryname', 'book.title')

    id = db.Column(db.Integer, primary_key=True)
    categoryname = db.Column(db.String(255))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book', secondary='book_category_association', back_populates='categories')

class BookCategoryAssociation(db.Model):
    __tablename__ = 'book_category_association'
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('book_category.id'), primary_key=True)

class Author(db.Model,SerializerMixin):

    serialize_only = ('authorname',)

    id = db.Column(db.Integer, primary_key=True)
    authorname = db.Column(db.String(255))

class Review(db.Model,SerializerMixin):

    serialize_only = ('comment', 'book.title', 'book.description', 'book.autorname')

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book = db.relationship('Book', backref='reviews')
    user = db.relationship('User', backref='reviews')
