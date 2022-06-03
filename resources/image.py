import os

from flask_restful import Resource
from flask_uploads import UploadNotAllowed
from flask import request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity

from libs import image_helper
from libs.strings import get_text
from schemas.image import ImageSchema

image_schema = ImageSchema()


class Image(Resource):
	@classmethod
	@jwt_required()
	def get(cls, filename):
		user_id = get_jwt_identity()
		folder = f"user_{user_id}"
		if not image_helper.is_filename_safe(filename):
			return {"message": get_text("ILLIGAL_FILENAME")}

		try:
			return send_file(image_helper.get_path(filename, folder=folder))
		except FileNotFoundError:
			return {"message": get_text("NOT_FOUND").format(filename)}

	@classmethod
	@jwt_required()
	def delete(self, filename):
		user_id = get_jwt_identity()
		folder = f"user_{user_id}"

		if not image_helper.is_filename_safe(filename):
			return {"message": get_text("ILLIGAL_FILENAME")}

		try:
			os.remove(image_helper.get_path(filename, folder=folder))
			return {"message": get_text("DELETED_SUCCESSFULLY").format(filename)}
		except FileNotFoundError:
			return {"message": get_text("NOT_FOUND").format(filename)}
		except:
			return {"message": get_text("ERROR_DELETING")}


class ImageUpload(Resource):
	@classmethod
	@jwt_required()
	def post(self):
		data = image_schema.load(request.files)
		user_id = get_jwt_identity()
		folder = f"user_{user_id}"
		try:
			image_path = image_helper.save_image(data['image'], folder=folder)
			basename = image_helper.get_basename(image_path)
			return {"message": get_text("IMAGE_UPLOADED").format(basename)}
		except UploadNotAllowed:
			extension = image_helper.get_extension(data['image'])
			return {"message": get_text("EXTENSION_NOT_ALLOWED").format(extension)}