import sqlite3

connection = sqlite3.connect('data.db')  # only 1 file for the whole database

cursor = connection.cursor()

create_table = "CREATE TABLE jobs (id int, company text, remote int)"
cursor.execute(create_table)

jobs = [(1, "Spotify", 1),
        (2, "Licorne", 1),
        (3, "Hermes", 0)]

insert_query = "INSERT INTO jobs VALUES (?, ?, ?)"
# cursor.execute(insert_query, job)
cursor.executemany(insert_query, jobs)

select_query = "SELECT * FROM jobs"
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()