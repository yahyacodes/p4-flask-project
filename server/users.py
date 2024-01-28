from flask import Flask, Blueprint, jsonify
from models import db, User
from flask_restful import Api, Resource, reqparse, abort
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (JWTManager, create_access_token, current_user, jwt_required)
from flask_jwt_extended import get_jwt_identity,get_jwt

app = Flask(__name__)
users_bp = Blueprint('User', __name__)
api = Api(users_bp)
ma = Marshmallow(users_bp)
bcrypt = Bcrypt()
bcrypt.init_app(app)
jwt = JWTManager(app)


patch_args = reqparse.RequestParser(bundle_errors = True)
patch_args.add_argument('id', type=int, help='Updted Id of the user')
patch_args.add_argument('name', type=str, help='Updated Name of the user')

post_args = reqparse.RequestParser()
# post_args.add_argument('id', type=int, help='Add Id of the user', required = True)
post_args.add_argument('username', type=str, help='Add Username of the user', required = True)
post_args.add_argument('email', type=str, help='Add Email of the user', required = True)
post_args.add_argument('password', type=str, help='Add Password of the user', required = True)

login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, required=True)
login_args.add_argument('password', type=str)

# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data['sub']
#     return User.query.filter_by(id = identity).one_or_none()

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()

user_schema = UserSchema()

class UserLogin(Resource):
    def get(self):
        return current_user.to_dict()

    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email = data.email).first()
        if not user:
            return abort(404, detail = 'User does not exist')
        if not bcrypt.check_password_hash(user.password, data.password):
            return abort(403, detail = 'Wrong Password')
        access_token = create_access_token(identity = user.id)
        return jsonify(access_token = access_token)
    
## User Routes
class UsersRescources(Resource):
    def get(self):
        users = User.query.all()
        response = [user.to_dict() for user in users]
        return response
    

    def post(self):
        data = post_args.parse_args()
        new_user = User(email = data.email, username = data.username, password = bcrypt.generate_password_hash(data.password))
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict()
    
class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id = id).first()
        return user_schema.dump(user)
    
    def patch(self, id):
        user = User.query.filter_by(id = id).first()
        data = patch_args.parse_args()
        for key, value in data.items():
            if value is None:
                continue
            setattr(user, key, value)
        db.session.commit()
        return user.to_dict()
    
    def delete(self, id):
        User.query.filter_by(id = id).delete()
        db.session.commit()
        return {'detail': 'User has been deleted successfully'}

api.add_resource(UserLogin, '/login')
api.add_resource(UsersRescources, '/users')
api.add_resource(UserById, '/users/<int:id>')