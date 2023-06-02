from flask import Flask, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import User, Package
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta


class CreatePackageController(Resource):
    def get(self):
        return "create custom get"

    def post(self):
        data = request.get_json()
        check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
        check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        encoded_jwt = jwt.decode(data["api_token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = encoded_jwt["user_id"]



        
        return 'success'
            