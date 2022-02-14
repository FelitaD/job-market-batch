from flask import Flask
from flask_restful import Api

from flask_jwt_extended import JWTManager

from user import UserRegister, UserLogin
from item import Job, JobList

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Job, '/job/<string:job_id>')
api.add_resource(JobList, '/jobs')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
