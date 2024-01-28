from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
from flask_cors import CORS
from books import books_bp
from users import users_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(books_bp)
app.register_blueprint(users_bp)
app.config["JWT_SECRET_KEY"] = "7de5f87982214b0a80dc8216443637f0"  
jwt = JWTManager(app)
CORS(app)

if __name__ == '__main__':
    app.run(port=5555)