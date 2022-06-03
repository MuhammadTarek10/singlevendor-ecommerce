from db import db
from uuid import uuid4
from time import time

CONFIRMATION_EXPIRATION_DELTA = 1800 #30 minutes

class ConfirmationModel(db.Model):
    __tablename__ = 'confirmations'

    id = db.Column(db.String(50), primary_key=True)
    expire_at = db.Column(db.Integer)
    confirmed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel", viewonly=True)

    def __init__(self, user_id, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA

    def json(self):
        return {"confirmed": self.confirmed, "expire_at": self.expire_at, "confirmation_id": self.id}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @property
    def expired(self):
        return time() > self.expire_at

    def force_to_expire(self):
        if not self.expired:
            self.expire_at = int(time())
            self.save_to_database()

    def save_to_database(self):
    	db.session.add(self)
    	db.session.commit()

    def delete_from_database(self):
    	db.session.delete(self)
    	db.session.commit()
