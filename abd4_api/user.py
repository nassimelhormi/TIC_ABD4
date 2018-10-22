from flask import Flask
from flask_restful import Resource, reqparse, Api
from flaskext.mysql import MySQL

# Creating MySQL instance
mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'vdm_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
api = Api(app)


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
        connection = mysql.connect()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = '{0}'".format(_username)
        print(_username)
        print(query)
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        cursor.close()
        connection.close()
        return user

    # This method find user with id in parameter
    # @param id (int)
    # @return user
    @classmethod
    def find_by_id(cls, _id):
        connection = mysql.connect()
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id_user = '{0}'".format(_id)
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

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
        connection = mysql.connect()
        cursor = connection.cursor

        if User.find_by_username(data['username']) is not None:
            cursor.close()
            connection.close()
            return {"message": "This user name already exist."}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))
        cursor.close()
        connection.close()
        return {"message": "User created successfully."}, 201
