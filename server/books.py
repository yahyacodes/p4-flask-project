from flask import Flask, Blueprint
from models import db, Book, Author, BookCategory, User
from flask_restful import Resource, Api, reqparse
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow
from flask_cors import cross_origin, CORS
from flask_jwt_extended import jwt_required


books_bp = Blueprint('books_blueprint', __name__)
api = Api(books_bp)
ma = Marshmallow(books_bp)
CORS(books_bp)

patch_args = reqparse.RequestParser(bundle_errors = True)
patch_args.add_argument('id', type=int, help='Updted Id of the user')
patch_args.add_argument('title', type=str, help='Add Title of the book')
patch_args.add_argument('description', type=str, help='Add Description of the book')
patch_args.add_argument('authorname', type=str, help='Add name of the Author of the book')
patch_args.add_argument('categoryname', type=str, help='Add name of the Category of the book')

post_args = reqparse.RequestParser(bundle_errors = True)
post_args.add_argument('title', type=str, help='Add Title of the book', required = True)
post_args.add_argument('description', type=str, help='Add Description of the book', required = True)
post_args.add_argument('authorname', type=str, help='Add name of the Author of the book', required = True)
post_args.add_argument('categoryname', type=str, help='Add name of the Author of the book', required = True)
post_args.add_argument('user_id', type=int, help='Add name of the Category of the book', required = True)

class BookSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Book
    id = ma.auto_field()
    title = ma.auto_field() 
    description = ma.auto_field()
    author_id = ma.auto_field()
    user_id = ma.auto_field()
    author = ma.Nested('AuthorSchema', only=['authorname'])
    user = ma.Nested('UserSchema', only=['username'])

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()

user_schema = UserSchema()

class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
    id = ma.auto_field()
    authorname = ma.auto_field()

user_schema = UserSchema()

book_schema = BookSchema()

## Books Routes

class BooksRescources(Resource):
    @jwt_required()
    def get(self):
        books = Book.query.all()
        response = [book.to_dict() for book in books]
        print(response)
        return response
    
    @jwt_required()
    def post(self):
        data = post_args.parse_args()

        # create author if not exist
        author = Author.query.filter_by(authorname = data['authorname']).first()
        if not author:
            author = Author(authorname = data['authorname'])
            db.session.add(author)

        # create category if not exist
        category = BookCategory.query.filter_by(categoryname = data['categoryname']).first()
        if not category:
            category = BookCategory(categoryname = data['categoryname'])
            db.session.add(category)

        # create book
        new_book = Book(title = data['title'], description = data['description'], author_id = author.id, user_id = data['user_id'])
        db.session.add(new_book)
        db.session.commit()

        # associate book with category
        new_book.categories.append(category)
        db.session.commit()

        return new_book.to_dict()
    
class BookById(Resource):
    @jwt_required()
    def get(self, id):
        book = Book.query.filter_by(id = id).first()
        return book_schema.dump(book)
    
    @jwt_required()
    def patch(self, id):
        book = Book.query.filter_by(id = id).first()
        data = patch_args.parse_args()
        for key, value in data.items():
            if value is None:
                continue
            setattr(book, key, value)
        db.session.commit()
        return book.to_dict()
    
    @jwt_required()
    def delete(self, id):
        Book.query.filter_by(id = id).delete()
        db.session.commit()
        return {'detail': 'Book has been deleted successfully'}
    
api.add_resource(BooksRescources, '/books')
api.add_resource(BookById, '/books/<int:id>')