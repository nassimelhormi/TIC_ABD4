import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create the "users" table
create_user_table = "CREATE TABLE IF NOT EXISTS users (id_user INTERGER PRIMARY KEY, username varchar(255), password text)"
cursor.execute(create_user_table)

# Insert a user in the "users" table
user = (34, 'jad04', 'root')
insert_user = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_user, user)

select_user = "SELECT * FROM users WHERE 1 = 1"
for row in cursor.execute(select_user):
    print(row)

#Create game table
create_game_table = """CREATE TABLE IF NOT EXISTS game (id_game INTERGER PRIMARY KEY,
                        name varchar(255))"""
cursor.execute(create_game_table)

#Insert  gmae in the game table
game = (31, 'mario odyssey06')
insert_game = "INSERT INTO game VALUES (?, ?)"
cursor.execute(insert_game, game)

select_game = "SELECT * FROM game"
for row in cursor.execute(select_game):
    print(row)

#create reservation table
create_reservation_table = """CREATE TABLE IF NOT EXISTS reservations (
    id_reservation INTEGER PRIMERY KEY, 
    day VARCHAR(45), 
    hour VARCHAR(45), 
    is_vr TinyInt(1) DEFAULT 0,
    id_game INTERGER NOT NULL,
    id_client INTERGER NOT NULL,
    FOREIGN KEY(id_game) REFERENCES games(id_game), 
    FOREIGN KEY(id_client) REFERENCES clients(id_client)
)"""
cursor.execute(create_reservation_table)

#insert reservations in the reservation table
reservation = (1, '22/10/18', '20:50', 1, 8, 9)
insert_reservation = "INSERT INTO reservations VALUES (?, ?, ?, ?, ?, ?)"
cursor.execute(insert_reservation, reservation)

select_reservation = "SELECT * FROM reservations"
for row in cursor.execute(select_reservation):
    print(row)

#create client table 
create_client_table = """CREATE TABLE IF NOT EXISTS clients
                        (id_client INTEGER PRIMERY KEY, 
                        gender TinyInt(1) DEFAULT 0,
                        age INTEGER, email VARCHAR(45))"""
cursor.execute(create_client_table)


#insert client in the client table 
client = (78, 'Femme', '90', 'jado78@gmail.com')
insert_client = "INSERT INTO clients VALUES (?, ?, ?, ?)"
cursor.execute(insert_client, client)

select_client = "SELECT * FROM clients"
for row in cursor.execute(select_client):
    print(row)

connection.commit()
connection.close()
