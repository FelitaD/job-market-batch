from flask import Flask, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import datetime

from api.resources.user import UserRegister, UserLogin
from api.resources.job import Job, JobList
from api.resources.company import Company, CompanyList
from api.db import db
from config.definitions import JOB_MARKET_DB_PWD, JOB_MARKET_DB_USER


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{JOB_MARKET_DB_USER}:{JOB_MARKET_DB_PWD}@localhost:5432/job_market'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # library has its own tracker
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
api = Api(app)
db.init_app(app)  # if app not run from command line

api.add_resource(Job, '/job/<int:id>')
api.add_resource(Company, '/company/<string:name>')
api.add_resource(JobList, '/jobs')
api.add_resource(CompanyList, '/companies')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def hello():
    return render_template('index.html', now=datetime.now())


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/comments/')
def comments():
    comments = ['This is the first comment.',
                'This is the second comment.',
                'This is the third comment.',
                'This is the fourth comment.'
                ]
    return render_template('comments.html', comments=comments)


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
