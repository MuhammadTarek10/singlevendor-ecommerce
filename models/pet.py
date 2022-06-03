from db import db

class PetModel(db.Model):
	__tablename__ = 'pets'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))

	user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
	user = db.relationship("UserModel", overlaps='pets')

	def __init__(self, name, user_id):
		self.name = name
		self.user_id = user_id


	def save_to_database(self):
		db.session.add(self)
		db.session.commit()