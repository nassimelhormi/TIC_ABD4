from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

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
    @jwt_required()
    def get(self, email):
        for reservation in reservations:
            if reservation["Acheteur"]["Email"] == email:
                return reservation["Acheteur"], 200
        return {"message": "Acheteur not found."}, 404

    @jwt_required()
    def post(self, email):
        data = request.get_json()
        acheteur = {"Civilite": data["Civilite"], "Nom": data["Nom"], "Prenom": data["Prenom"], "Age": data["Age"], "Email": email}

        reservations.append({"Acheteur": acheteur})
        return {"Acheteur": acheteur}, 201

class ReservationList(Resource):
    @jwt_required()
    def get(self):
        return reservations

api.add_resource(Acheteur, '/acheteur/<string:email>') # http://localhost:4242/acheteur/nassimelhormi@dailymotion.com
api.add_resource(ReservationList, '/reservations')

app.run(port=4242)