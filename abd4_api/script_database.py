import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create the "users" table
create_user_table = "CREATE TABLE IF NOT EXISTS users (id_user INTERGER PRIMARY KEY, username varchar(255), password text)"
cursor.execute(create_user_table)

# Insert a user in the "users" table
user = (29, 'samir', 'root')
insert_user = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_user, user)

select_user = "SELECT * FROM users WHERE 1 = 1"
for row in cursor.execute(select_user):
    print(row)

#Create game table
create_game_table = "CREATE TABLE IF NOT EXISTS game (id_game INTERGER PRIMARY KEY,name varchar(255))"
cursor.execute(create_game_table)

#Insert a gmae in the game table
game = (1, 'Interminable attente chez le medecin')
insert_game = "INSERT INTO game VALUES (?, ?)"
cursor.execute(insert_game, game)

select_game = "SELECT * FROM game"
for row in cursor.execute(select_game):
    print(row)

connection.commit()
connection.close()
