from db import db
import numpy as np

class ProductModel(db.Model):
	__tablename__ = 'products'

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	name = db.Column(db.String(30), nullable=False)
	price = db.Column(db.Float, nullable=False)
	available = db.Column(db.Boolean, default=True)
	description = db.Column(db.String(120))
	genre = db.Column(db.String(20))

	rate = db.relationship("RateModel", lazy="dynamic")

	def __init__(self, name, price, description, genre, available=True):
		self.name = name
		self.price = price
		self.available = available
		self.description = description
		self.genre = genre

	def json(self):
		return {"name": self.name, "price": self.price, "genre": self.genre, "available": self.available, "rate": self.get_rate()}

	def save_to_database(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_database(self):
		db.session.delete(self)
		db.session.commit()

	def get_rate(self):
		rates = []
		for r in self.rate:
			rates.append(r.rate)

		if len(rates) != 0:
			return np.mean(rates)

		return None

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first()

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	@classmethod
	def find_by_genre(cls, genre):
		return cls.query.filter_by(genre=genre).all()

	@classmethod
	def find_price_greater(cls, price):
		return cls.query.filter(price>=price).all()

	@classmethod
	def find_price_smaller(cls, price):
		return cls.query.filter(price<=price).all()