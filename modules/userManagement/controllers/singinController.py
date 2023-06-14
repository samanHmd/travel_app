from flask import request
from flask_restful import Resource
from modules.userManagement.models.user import User



class SignInController(Resource):
    def get(self):
        users = User.query.all()
        return users

    def post(self):
        data = request.get_json()
        register_response = User.register(data)
        return register_response
            

        