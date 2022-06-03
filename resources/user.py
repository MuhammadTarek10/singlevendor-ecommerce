from flask_restful import Resource, reqparse
from flask_jwt_extended import (
        create_access_token,
        create_refresh_token,
        jwt_required,
        get_jwt_identity,
    )
from libs.strings import get_text
from models.user import UserModel
from libs.mailgun import MailGunException
from models.confirmation import ConfirmationModel


class User(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('first_name', type=str, required=True)
    parser.add_argument('last_name', type=str, required=True)
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('email', type=str, required=True)

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": get_text("NOT_FOUND").format("user")}

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": get_text("NOT_FOUND").format("user")}

        try:
            user.delete_from_database()
        except:
            return {"message": get_text("ERROR_DELETING")}


class UserLogin(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self):
        user_data = self.parser.parse_args()

        user = UserModel.find_by_username(user_data['username'])



        if not user:
            return {"message": get_text("INVALID_INPUTS")}

        if user.password == user_data['password']:
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
        return {"message": get_text("ACCOUNT_NOT_ACTIVE")}


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('first_name', type=str, required=True)
    parser.add_argument('last_name', type=str, required=True)
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    parser.add_argument('email', type=str, required=True)

    def post(self):
        user_data = self.parser.parse_args()

        if UserModel.find_by_username(user_data['username']):
            return {"message": get_text("ALREADY_TAKEN").format("username")}

        if UserModel.find_by_email(user_data['email']):
            return {"message": get_text("ALREADY_TAKEN").format("email")}

        user = UserModel(**user_data)

        try:
            user.save_to_database()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_database()
            user.send_confirmation_email()
            return {"message": get_text("SENT_CONFIRMATION_MAIL")}, 201
        except MailGunException as e:
            user.delete_from_database()
            return {"message": str(e)}, 500
        except:
            user.delete_from_database()
            return {"message": get_text("ERROR_ADDING")}


class UserList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        users = [user.json() for user in UserModel.query.all()]
        user_id = get_jwt_identity()
        try:
            username = UserModel.find_by_id(user_id).username
        except:
            username = None
        return {"Users": users, "request from": username}
