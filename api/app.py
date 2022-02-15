from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserLogin
from resources.job import Job, JobList
from resources.company import Company, CompanyList
from db import db


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # library has its own tracker
app.config['SECRET_KEY'] = 'super-secret'
api = Api(app)
db.init_app(app) # if app not  run from command line


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

jwt = JWTManager(app)

api.add_resource(Job, '/job/<int:id>')
api.add_resource(Company, '/company/<string:name>')
api.add_resource(JobList, '/jobs')
api.add_resource(CompanyList, '/companies')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
