from flask_restful import Resource, reqparse, inputs

from libs.strings import get_text
from models.product import ProductModel

class Product(Resource):
	def get(self, name):
		product = ProductModel.find_by_name(name)

		if not product:
			return {"message": get_text("NOT_FOUND").format("name")}

		return {"Product": product.json()}


class ProductRegister(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('name', type=str, required=True)
	parser.add_argument('price', type=float, required=True)
	parser.add_argument('description', type=str)
	parser.add_argument('genre', type=str, required=True)
	parser.add_argument('available', type=inputs.boolean)

	def post(self):
		product_data = self.parser.parse_args()

		try:
			product = ProductModel(**product_data)
		except:
			return {"message": get_text("ERROR_CREATING_PRODUCT")}

		if product.price < 0:
			return {"message": get_text("CANT_INPUT_NEGATIVE")}

		if ProductModel.find_by_name(product.name):
			return {"message": get_text("ALREADY_TAKEN").format(product.name)}

		try:
			product.save_to_database()
			return {"message": get_text("CREATED_SUCCESSFULLY").format(product.name)}
		except:
			return {"message": get_text("ERROR_ADDING")}

class ProductModify(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('name', type=str, required=True)
	parser.add_argument('price', type=float)
	parser.add_argument('description', type=str)
	parser.add_argument('genre', type=str)
	parser.add_argument('available', type=inputs.boolean)

	def put(self):
		product_data = self.parser.parse_args()

		product = ProductModel.find_by_name(product_data['name'])

		if product.price != product_data['price']:
			product.price = product_data['price']

		if product.available != product_data['available']:
			product.available = product_data['available']

		if product.genre != product_data['genre']:
			product.genre = product_data['genre']

		if product.description != product_data['description']:
			product.description = product_data['description']

		try:
			product.save_to_database()
		except:
			return {"message": get_text("ERROR_ADDING")}

		return {"message": get_text("DONE_MODIFICATIONS")}


class ProductGenre(Resource):
	def get(self, genre):
		products = ProductModel.find_by_genre(genre)

		if not products:
			return {"message": get_text("NOT_FOUND").format("genre")}

		return {"Products": [product.json() for product in products]}


class ProductPrice(Resource):
	def get(self, price):
		products = ProductModel.find_price_greater(price)

		if not products:
			return {"message": get_text("NOT_FOUND").format("price")}

		return {"Products": [product.json() for product in products]}


class ProductList(Resource):
	def get(self):
		return {"Products": [product.json() for product in ProductModel.query.all()]}