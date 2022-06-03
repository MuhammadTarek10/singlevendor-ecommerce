from flask_restful import Resource, reqparse

from libs.strings import get_text
from models.pet import PetModel
from models.user import UserModel

class Pet(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('name', type=str, required=True)
	parser.add_argument('user_id', type=int, required=True)

	def post(self):
		pet_data = self.parser.parse_args()

		if not UserModel.find_by_id(pet_data['user_id']):
			return {"message": get_text("DIDNT_FIND_USER")}

		pet = PetModel(**pet_data)
		
		pet.save_to_database()
		return {"message": get_text("CREATED_SUCCESSFULLY").format(pet_data['name'])}