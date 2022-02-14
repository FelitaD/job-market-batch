import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required


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
    def get(self, job_id):
        connection = sqlite3.connect('/Users/donor/PycharmProjects/DE_job_market/api/data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM jobs WHERE id = ?"
        result = cursor.execute(query, (job_id,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'job': {'company': row[0], 'remote': row[1]}}
        return {'message': 'Item not found'}, 404

    def post(self, job_id):
        if next(filter(lambda x: x['job_id'] == job_id, jobs), None) is not None:
            return {'message': "A job with id '{}' already exists.".format(job_id)}, 400  # Bad Request, client's fault (should have checked if item existed)

        data = Job.parser.parse_args()

        job = {'job_id': job_id, 'remote': data['remote'], 'company': data['company']}
        jobs.append(job)
        return job, 201

    @jwt_required()
    def delete(self, job_id):
        global jobs
        jobs = list(filter(lambda x: x['job_id'] != job_id, jobs))
        return {'message': 'Job deleted'}

    @jwt_required()
    def put(self, job_id):
        data = Job.parser.parse_args()

        job = next(filter(lambda x: x['job_id'] == job_id, jobs), None)
        if job is None:
            job = {'job_id': job_id, 'remote': data['remote'], 'company': data['company']}
            jobs.append(job)
        else:
            job.update(data)
        return job


class JobList(Resource):
    def get(self):
        return {'jobs': jobs}
