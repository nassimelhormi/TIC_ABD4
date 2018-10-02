from flask_restful import Resource, reqparse
import sqlite3

class User:

    def __init__(self, _id, _username, _password):
        self.id = _id
        self.username = _username
        self.password = _password

    # This method find user with username in parameter
    # @param username (str)
    # @return user
    @classmethod
    def find_by_username(cls, _username):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(query, (_username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    # This method find user with id in parameter
    # @param id (int)
    # @return user
    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id_user = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

class UserRegister(Resource):

    # fields required to register
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    # post method insert user into the database
    # @param self
    # @return 201
    def post(self):
        data = UserRegister.parser.parse_args()
        connection = slite3.connect('database.db')
        cursor = connection.cursor

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
