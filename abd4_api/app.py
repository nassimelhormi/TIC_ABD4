from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from flaskext.mysql import MySQL
import pprint
from security import authenticate, identity
from user import UserRegister

# Creating MySQL instance
mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'nassim'
mysql.init_app(app)
api = Api(app)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'vdm_db'
app.config['MYSQL_DATABASE_HOST'] = 'mysqlmaster'

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

def create_reservation(day, hour, is_vr, g_name):

    connection = mysql.connect()
    cursor = connection.cursor()
    insert_reservation = "INSERT INTO reservations(day, hour, is_vr,g_name)  VALUES (%s, %s, %s, %s)"
    reservations = (day,hour,is_vr,g_name,)
    cursor.execute(insert_reservation, reservations)
    select_reservation = "SELECT  LAST_INSERT_ID();"
    cursor.execute(select_reservation)
    rows = cursor.fetchall()
    id_reservation = rows[0]
    connection.commit()
    connection.close()
    return (id_reservation)

def get_clients(json_data):
    client_list = []
    acheteur = json_data['Acheteur']
    k = {
        'gender' : acheteur['Civilite'],
        'age'    : acheteur['Age'],
        'email'  : acheteur['Email'],
        'first_name': acheteur['Nom'],
        'last_name' : acheteur['Prenom'],
        'is_acheteur' : True
    }
    for reservation in json_data['Reservation']:
        d = {
            'gender' : reservation['Spectateur']['Civilite'],
            'age'    : reservation['Spectateur']['Age'],
            'email'  : '',
            'first_name': reservation['Spectateur']['Nom'],
            'last_name' : reservation['Spectateur']['Prenom'],
            'tarif'    : reservation['Tarif'],
            'is_acheteur' : False
        }
        if (d['first_name'] != k['first_name'] and d['last_name'] != k['last_name']):
            client_list.append(d)
        else:
            k['tarif'] = reservation['Tarif']
    client_list.append(k)
    return client_list
        
def find_client(gender, first_name, last_name):
    connection = mysql.connect()
    cursor = connection.cursor()
    clt_selected_tuple = (gender, first_name, last_name,)
    select_client = "SELECT id_client FROM Clients WHERE gender = %s AND first_name = %s AND last_name = %s"
    cursor.execute(select_client,clt_selected_tuple)
    rows = cursor.fetchall()
    pprint.pprint(rows)
    connection.commit()
    connection.close()
    if len(rows) == 1:
        return rows[0]
    return None

def insert_clients(list_clients):
    connection = mysql.connect()
    cursor = connection.cursor()
    list_ids = []
    for client in list_clients:
        founded_client = find_client(client['gender'],client['first_name'],client['last_name'])
        print("founded_client = {}".format(founded_client))
        if founded_client == None:
            try:
                clients_tuple = (client['gender'],client['age'],client['email'],client['first_name'],client['last_name'],client['tarif'],client['is_acheteur'],)
                insert_query = "INSERT INTO Clients(gender,age,email,first_name,last_name,tarif,is_acheteur) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, clients_tuple)
                select_id_client = "SELECT  LAST_INSERT_ID();"
                cursor.execute(select_id_client)
                rows = cursor.fetchall()
                inserted_client = rows[0][0]
                print("inserted_client ->", inserted_client)
                list_ids.append(inserted_client)
            except Exception as e:
                print("Exception ----> {}".format(str(e)))
        else:
            list_ids.append(founded_client)

    connection.commit()
    connection.close()
    print("c'est de la merde ici ------>")
    pprint.pprint(list_ids)
    return list_ids
    

def insert_spectateurs(list_ids,id_reservation):
    connection = mysql.connect()
    cursor = connection.cursor()
    pprint.pprint(list_ids)
    for id_clients in list_ids:
        spect_tuple = (id_clients, id_reservation,)
        query = "INSERT INTO Spectateurs(id_client,id_reservation) VALUES(%s, %s)"
        print(query)
        print(spect_tuple)
        cursor.execute(query, spect_tuple)
    connection.commit()
    connection.close()

class booking(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        day = json_data['Game']['Jour']
        hour = json_data['Game']['Horaire']
        is_vr = 1 if json_data['Game']['VR'] == "Non" else 0
        g_name = json_data['Game']['Nom']

        id_reservation = create_reservation(day,hour,is_vr,g_name)
        client_list = get_clients(json_data)
        insered_clients = insert_clients(client_list)
        insert_spectateurs(insered_clients,id_reservation) 
        return {'id': id_reservation,'day': day, 'hour': hour, 'is_vr': is_vr, 'g_name': g_name}, 201 
        



api.add_resource(booking, '/booking')
app.run(host='0.0.0.0', port=5000, debug=True)
