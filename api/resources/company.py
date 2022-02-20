from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from api.models.company import CompanyModel


class Company(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='This field cannot be left blank !')

    @jwt_required()
    def get(self, name):
        company = CompanyModel.find_by_name(name)
        if company:
            return company.json()
        return {'message': 'Company not found'}, 404

    @jwt_required()
    def post(self, name):
        if CompanyModel.find_by_name(name):
            return {'message': 'A company named {} already exists'.format(name)}, 400

        company = CompanyModel(name)
        try:
            company.save_to_db()
        except:
            return {'message': 'An error occured'}, 500

        return company.json(), 201

    @jwt_required()
    def delete(self, name):
        company = CompanyModel.find_by_name(name)
        if company:
            company.delete_from_db()

        return {'message': 'Company deleted'}


class CompanyList(Resource):
    def get(self):
        return {'companies': [company.json() for company in CompanyModel.query.all()]}
