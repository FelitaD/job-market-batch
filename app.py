from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

jobs = []


class Job(Resource):
    def get(self, job_id):
        job = next(filter(lambda x: x['job_id'] == job_id, jobs), None)
        return {'job': job}, 200 if job else 404

    def post(self, job_id):
        if next(filter(lambda x: x['job_id'] == job_id, jobs), None) is not None:
            return {'message': "A job with id '{}' already exists.".format(job_id)}, 400  # Bad Request, client's fault (should have checked if item existed)

        data = request.get_json()  # gets data from the payload in the request
        job = {'job_id': job_id, 'remote': data['remote'], 'company': data['company']}
        jobs.append(job)
        return job, 201

    def delete(self, job_id):
        global jobs
        jobs = list(filter(lambda x: x['job_id'] != job_id, jobs))
        return {'message': 'Job deleted'}

    def put(self, job_id):
        data = request.get_json()
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


api.add_resource(Job, '/job/<string:job_id>')
api.add_resource(JobList, '/jobs')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
