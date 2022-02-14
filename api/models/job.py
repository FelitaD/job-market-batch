import sqlite3

# methods that the client don't need to interact with directly
class JobModel:
    def __init__(self, id, company, remote):
        self.id = id
        self.company = company
        self.remote = remote

    def json(self):
        return {'id': self.id, 'company': self.company, 'remote': self.remote}

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM jobs WHERE id = ?"
        result = cursor.execute(query, (id,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(row[1], row[1], row[2])

    def insert(self):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "INSERT INTO jobs VALUES (?, ?, ?)"
        cursor.execute(query, (self.id, self.company, self.remote))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "UPDATE jobs SET company = ? WHERE id = ?"
        cursor.execute(query, (self.company, self.id))
        connection.commit()
        connection.close()