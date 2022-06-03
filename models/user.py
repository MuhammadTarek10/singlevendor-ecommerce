from db import db

from flask import request, url_for
from models.confirmation import ConfirmationModel
from libs.mailgun import Mailgun

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    rate = db.relationship("RateModel")
    confirmation = db.relationship("ConfirmationModel", lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, username, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

    def json(self):
        return {"first_name": self.first_name, "username": self.username, "email": self.email}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @property
    def most_recent_confirmation(self):
        return self.confirmation.order_by(db.desc(ConfirmationModel.expire_at)).first()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)
        subject = "Registration Confirmation"
        text = f"Hi, Click the link to confirm Registration: {link}"
        html = f'<html>Hi, Click the link to confirm Registration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_email([self.email], subject, text, html)

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()
