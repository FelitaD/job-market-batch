import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from models.job import JobModel

class Job(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('company',
                        type=str,
                        required=True,
                        help='This field cannot be left blank !')
    parser.add_argument('remote',
                        type=int,
                        required=False)

    @jwt_required()
    def get(self, id):
        job = JobModel.find_by_id(id)
        if job:
            return job.json()
        return {'message': 'Item not found'}, 404

    def post(self, id):
        if JobModel.find_by_id(id):
            return {'message': "A job with id '{}' already exists.".format(id)}, 400  # Bad Request, client's fault (should have checked if item existed)

        data = Job.parser.parse_args()
        job = JobModel(id, data['company'], data['remote'])

        try:
            job.insert()
        except:
            return {'message': "An error occured"}, 500

        return job.json(), 201

    @jwt_required()
    def delete(self, id):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "DELETE FROM jobs WHERE id = ?"
        result = cursor.execute(query, (id,))
        connection.commit()
        connection.close()

        return {'message': 'Job deleted'}

    @jwt_required()
    def put(self, id):
        data = Job.parser.parse_args()

        job = JobModel.find_by_id(id)
        updated_job = JobModel(id, data['company'], data['remote'])

        if job is None :
            try:
                updated_job.insert()
            except:
                return {'message': 'Error inserting job'}, 500
        else :
            try:
                updated_job.update()
            except:
                return {'message': 'Error updating job'}, 500
        return updated_job.json()


class JobList(Resource):
    def get(self):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        results = cursor.execute("SELECT * FROM jobs")
        jobs = []
        for row in results:
            jobs.append({'id': row[0], 'company': row[1], 'remote': row[2]})
        connection.close()
        return {'jobs': jobs}
