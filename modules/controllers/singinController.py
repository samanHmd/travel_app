from flask import Flask, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import User, Package
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta


class SignInController(Resource):
    def get(self):
        users = User.query.all()
        return users

    def post(self):
        data = request.get_json()
        try:
            password = data.get('password')
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=data.get('name'), userName=data.get('userName'), email=data.get('email'), password=hashed)
            db.session.add(user)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return {'error': str(e)}, 400
        finally:
            db.session.commit()
            user = User.query.filter_by(userName=data.get('userName')).first()
            packages = Package.query.all()
            expiration_time = (datetime.utcnow() + timedelta(seconds=172800)).isoformat()
            encoded_jwt = jwt.encode({'user_id':user.id, 'expiration': expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
            return {"status": "success","api_token": encoded_jwt, "packages": [package.as_dict() for package in packages], "userName": user.userName}, 200
            

        