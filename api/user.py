import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity
from hmac import compare_digest

_user_parser = reqparse.RequestParser() # _ you should not import it from somewhere else because private
_user_parser.add_argument('username', type=str, required=True, help="This field cannot be blank")
_user_parser.add_argument('password', type=str, required=True, help="This field cannot be blank")


class User(object):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (username,)) # ? matches a tuple (,)
        row = result.fetchone()
        if row:
            user = cls(*row) # *extends : matches number of arguments in __init__
            # user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (_id,))  # ? matches a tuple (,)
        row = result.fetchone()
        if row:
            user = cls(*row)  # *extends : matches number of arguments in __init__
            # user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created succesfully."}, 201


class UserLogin(Resource):
    # Endpoint to authenticate

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database
        user = User.find_by_username(data['username'])

        # check password
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials'}, 401

        # create access token
        # create refresh token

