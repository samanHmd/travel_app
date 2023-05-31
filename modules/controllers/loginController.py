from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.Models import User, Package
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta





class LoginController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_jwt

    def post(self):
        data = request.get_json()
        user = User.query.filter_by(userName=data.get('userName')).first()
        packages = Package.query.all()
        if user and bcrypt.check_password_hash(user.password, data.get('password')):
            encoded_jwt = jwt.encode({'user_id':user.id, 'expiration': str(datetime.utcnow() + timedelta(seconds=172800))}, app.config['SECRET_KEY'], algorithm="HS256")
            return {"status": "success","api_token": encoded_jwt, "packages": jsonify([package.as_dict() for package in packages])}, 200
        else:
            return { "status": "fail" }