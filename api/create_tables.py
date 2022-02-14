import sqlite3

connection = sqlite3.connect('data.db')  # only 1 file for the whole database

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, company text, remote int)"
cursor.execute(create_table)

connection.commit()
connection.close()