import os
from dotenv import load_dotenv

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_uploads import configure_uploads

from db import db
from resources.user import User, UserLogin, UserList, UserRegister
from resources.product import Product, ProductModify, ProductRegister, ProductPrice, ProductGenre, ProductList
from resources.rate import Rate
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.image import ImageUpload, Image
from libs.image_helper import IMAGE_SET


app = Flask(__name__)
load_dotenv(".env", verbose=True)

JWT_SECRET_KEY = "Tarek"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db/"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object("default_config")
configure_uploads(app, IMAGE_SET)

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(UserRegister, '/user/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(Confirmation, '/confirm/<string:confirmation_id>')
api.add_resource(ConfirmationByUser, '/confirm/user')
api.add_resource(UserList, '/users')
api.add_resource(ProductRegister, '/product/regitser')
api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(Product, '/product/<string:name>')
api.add_resource(ProductModify, '/product/modify')
api.add_resource(ProductList, '/products')
api.add_resource(ProductGenre, '/product/genre/<string:genre>')
api.add_resource(ProductPrice, '/product/price/<float:price>')
api.add_resource(Rate, '/rate')


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
