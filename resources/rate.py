from flask_restful import Resource, reqparse
from flask_jwt_extended import (
        jwt_required,
        get_jwt_identity,
    )

from libs.strings import get_text
from models.rate import RateModel
from models.product import ProductModel
from models.user import UserModel

class Rate(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('product_id', type=int, required=True)
	parser.add_argument('rate', type=float, required=True)


	@jwt_required()
	def post(self):
		rate_data = self.parser.parse_args()
		user_id = get_jwt_identity()
		product = ProductModel.find_by_id(rate_data['product_id'])

		if not product:
			return {"message": get_text("NOT_FOUND").format("prodcut")}

		if RateModel.already_rated(user_id, rate_data['product_id']):
			return {"message": get_text("ALREADY_RATED")}


		rate = RateModel(user_id, **rate_data)

		try:
			rate.save_to_database()
			return {"message": get_text("CREATED_SUCCESSFULLY").format("rate")}
		except:
			return {"message": get_text("ERROR_ADDING")}
