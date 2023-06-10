from flask import request
from flask_restful import Resource
from modules.userManagement.models.user import User
from modules.packageManagement.models.package import Package
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError


class SignInController(Resource):
    def get(self):
        users = User.query.all()
        return users

    def post(self):
        data = request.get_json()
        required_fields = ['userName', 'name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            
        if len(data['password']) < 5:
            return {"error": "Password should be at least 5 characters."}, 400
        
        existing_user_username = User.query.filter_by(userName=data.get('userName')).first()
        existing_user_email = User.query.filter_by(email=data.get('email')).first()

        if existing_user_username or existing_user_email:
            return {'error': 'Username or email already exists.'}, 400
            
        try:
            password = data.get('password')
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=data.get('name'), userName=data.get('userName'), email=data.get('email'), password=hashed)
            db.session.add(user)
            db.session.commit()
            db.session.flush()
        except IntegrityError as ie:
            print("IntegrityError: ", ie) # Let's print the error message
            db.session.rollback()
            return {'error': 'Username or email already exists.'}, 400
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return {'error': str(e)}, 400
        finally:
            user = User.query.filter_by(userName=data.get('userName')).first()
            packages = Package.query.all()
            expiration_time = (datetime.utcnow() + timedelta(seconds=172800)).isoformat()
            encoded_jwt = jwt.encode({'user_id':user.id, 'expiration': expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
            return {"status": "success","api_token": encoded_jwt, "packages": [package.as_dict() for package in packages], "userName": user.userName}, 200
            

        