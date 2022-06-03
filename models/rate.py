from db import db

class RateModel(db.Model):
	__tablename__ = "rates"

	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
	rate = db.Column(db.Float, nullable=False)

	user = db.relationship("UserModel", viewonly=True)
	product = db.relationship("ProductModel", viewonly=True)

	def __init__(self, user_id, product_id, rate):
		self.user_id = user_id
		self.product_id = product_id
		self.rate = rate

	def save_to_database(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def already_rated(cls, user_id, product_id):
		user = cls.query.filter_by(user_id=user_id).all()
		print(user)

		if user:
			for rate in user:
				if rate.product_id == product_id:
					return True

		return False
