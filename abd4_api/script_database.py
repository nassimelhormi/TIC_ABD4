import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create the "users" table
create_user_table = "CREATE TABLE users (id_user int, username text, password text)"
cursor.execute(create_user_table)

# Insert a user in the "users" table
user = (18, 'nassim', 'root')
insert_user = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_user, user)

select_user = "SELECT * FROM users WHERE 1 = 1"
for row in cursor.execute(select_user):
    print(row)

connection.commit()
connection.close()