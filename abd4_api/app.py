from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
import pprint
from security import authenticate, identity
from user import UserRegister
import sqlite3


app = Flask(__name__)
app.secret_key = 'nassim'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

reservations = [
    {
        "Acheteur":
        {
            "Civilite": "Monsieur",
            "Nom": "Carmine",
            "Prenom": "Art",
            "Age": 64,
            "Email": "carmine.art@gogole.com"
        },
        "Game":
        {
            "Nom": "Interminable attente chez le medecin",
            "Jour": "2018-09-07",
            "Horaire": "05:30",
            "VR": "Non"
        },
        "Reservation":
        [
            {
                "Spectateur":
                {
                    "Civilite": "Monsieur",
                    "Nom": "Carmine",
                    "Prenom": "Art",
                    "Age": 64
                },
                "Tarif": "Senior"
            },
            {
                "Spectateur":
                {
                    "Civilite": "Madame",
                    "Nom": "Nya",
                    "Prenom": "Kayla",
                    "Age": 22
                },
                "Tarif": "Plein tarif"
            }
        ]
    }
]

class Acheteur(Resource):
    #@jwt_required() #decorateur
    def get(self, email):
        for reservation in reservations:
            if reservation["Acheteur"]["Email"] == email:
                return reservation["Acheteur"], 200
        return {"message": "Acheteur not found."}, 404

    #@jwt_required()
    def post(self, email):
        data = request.get_json()
        acheteur = {"Civilite": data["Civilite"], "Nom": data["Nom"], "Prenom": data["Prenom"], "Age": data["Age"], "Email": email}

        reservations.append({"Acheteur": acheteur})
        return {"Acheteur": acheteur}, 201

class GameList(Resource):

    def get(self):
        response = []

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_game = "SELECT * FROM game"
        for row in cursor.execute(select_game):
            response.append({'id': row[0], 'title': row[1]})
        connection.commit()
        connection.close()
        return response,200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()
        game = (args['name'],)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        insert_game = "INSERT INTO game(name) VALUES (?)"
        cursor.execute(insert_game, game)
        select_game = "SELECT last_insert_rowid()"
        for row in cursor.execute(select_game):
            last_insert_id = row[0]
        pprint.pprint(args)
        connection.commit()
        connection.close()
        return {'id': last_insert_id,'name': args['name']}, 201

class Game(Resource):
    def get(self, id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_game = "SELECT * FROM game WHERE id_game = {}".format(id)
        for row in cursor.execute(select_game):
            return {'id_game': row[0], 'name': row[1]}, 200
        connection.commit()
        connection.close()
        return {'message': 'game not found'}, 404


class ClientList(Resource):

    def get(self):
        response = []

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_client = "SELECT * FROM clients"
        for row in cursor.execute(select_client):
            pprint.pprint(row)
            response.append({'id': row[0], 'gender': row[1], 'age': row[2], 'email': row[3]})
        connection.commit()
        connection.close()
        return response,200   
   
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('gender')
        parser.add_argument('age')
        parser.add_argument('email')
        args = parser.parse_args()
        clients = (args['gender'],args['age'], args['email'],)
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        insert_client = "INSERT INTO clients(gender, age, email)  VALUES (?, ?, ?)"
        cursor.execute(insert_client, clients)
        select_client = "SELECT last_insert_rowid()"
        for row in cursor.execute(select_client):
            last_insert_id = row[0]
        pprint.pprint(args)
        connection.commit()
        connection.close()
        return {'id': last_insert_id,'gender': args['gender'], 'age': args['age'], 'email': args['email']}, 201   

class ReservationList(Resource):
    def get(self):
        response = []

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        select_reservation = "SELECT * FROM reservations"
        for row in cursor.execute(select_reservation):
            pprint.pprint(row)
            response.append({'id': row[0], 'day': row[1], 'hour': row[2], 'is_vr': row[3], 'rate': row[4], 'id_game': row[5], 'id_client': row[5]})
        connection.commit()
        connection.close()
        return response,200  

api.add_resource(Acheteur, '/acheteur/<string:email>') # http://localhost:4242/acheteur/nassimelhormi@dailymotion.com
api.add_resource(ReservationList, '/reservations')
api.add_resource(UserRegister, '/register')
api.add_resource(GameList, '/games')
api.add_resource(Game, '/games/<int:id>')
api.add_resource(ClientList, '/clients')
app.run(port=4242, debug=True)
