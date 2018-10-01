from flask import Flask, jsonify, request

app =  Flask(__name__)

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

@app.route('/')
def home():
    return "The Début"

# post reservation
# @app.route('/reservation', methods=['POST'])
# def create_reservation():
#     request_data = request.get_json()
#     new_reservation = {
#         "Acheteur": request_data["Acheteur"],
#         "Game": request_data["Game"],
#         "Reservation": []
#     }
#     reservations.append(new_reservation)
#     return jsonify(new_reservation)




# get all the reservations
@app.route('/reservations')
def get_all_reservations():
    return jsonify({"reservation": reservations})

app.run(port=4242)