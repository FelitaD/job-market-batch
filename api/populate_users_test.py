import sqlite3

connection = sqlite3.connect('data.db')  # only 1 file for the whole database

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username company text, password text)"
cursor.execute(create_table)

users = [(1, "felita", "pate"),
        (2, "jose", "poulet"),
        (3, "roddy", "riz")]

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.execute(insert_query, job)
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()