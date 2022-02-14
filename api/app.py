from flask import Flask
from flask_restful import Api
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager

from user import UserRegister
from item import Job, JobList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWTManager(app)



api.add_resource(Job, '/job/<string:job_id>')
api.add_resource(JobList, '/jobs')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
