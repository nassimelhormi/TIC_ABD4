from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import booking
import logging
from redis import Redis
from rq import Queue

# Creating MySQL instance
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Flask(__name__)
api = Api(app)

q = Queue(connection=Redis(host="redis"))

RESERVATIONS = [
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


class bookingSTATS(Resource):

    def get(self):
        plein = booking.select_booking_stats("Plein tarif")
        etudiant = booking.select_booking_stats("Tarif etudiant")
        reduit = booking.select_booking_stats("Plein reduit")
        senior = booking.select_booking_stats("Senior")
        res = {
            "plein": plein,
            "etudiant": etudiant,
            "reduit": reduit,
            "senior": senior
        }
        return {"message": "ok", "results": res}, 200


class bookingNAME(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = bookingNAME.parser.parse_args()

        if (data['name']):
            res = booking.select_bookings_by_name(data["name"])
            return {"message": "ok", "results": res}, 200
        else:
            return {"message": "Something goes wrong"}, 401


class bookingDATE(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date_start', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('date_end', type=str, required=True, help="This field cannot be blank.")

    def get(self):
        data = bookingDATE.parser.parse_args()

        res = booking.select_bookings_by_date(data["date_start"], data["date_end"])
        return {"message": "ok", "results": res}, 200


class bookingALL(Resource):
    def get(self):
        res = booking.select_all_bookings()

        if res:
            return {"message": "ok", "results": res}, 200
        return {"message": "Something goes wrong"}, 401


class bookingCOUNT(Resource):
    def get(self):
        res = booking.count_all_bookings()

        if res:
            return {"message": "ok", "results": res}, 200
        return {"message": "Something goes wrong"}, 401


class bookingREST(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        # result = booking.process(json_data)
        job = q.enqueue(booking.process, json_data)
        return {"status": job.status, "job_id": job.id}, 201


class ping(Resource):
    def get(self):
        logging.info("test")
        return {"ping": "ok"}


api.add_resource(ping, '/ping')
api.add_resource(bookingSTATS, '/stats')
api.add_resource(bookingDATE, '/between')
api.add_resource(bookingNAME, '/search')
api.add_resource(bookingALL, '/all')
api.add_resource(bookingCOUNT, '/count')
api.add_resource(bookingREST, '/booking')
app.run(host='0.0.0.0', port=5000, debug=True)
