from modules import db, app
from datetime import datetime
from flask import Flask, jsonify
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules import bcrypt, app
from datetime import datetime, timedelta
import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
from modules import db, app
import stripe
from sqlalchemy import inspect
import logging


stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, userName={self.userName}, email={self.email})"

    def login(data):
        from modules.packageManagement.models.package import Package
        required_fields = ['userName', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            

        user = User.query.filter_by(userName=data.get('userName')).first()
        packages = Package.query.all()
        if user:
            if bcrypt.check_password_hash(user.password, data.get('password')):
                expiration_time = (datetime.utcnow() + timedelta(seconds=172800)).isoformat()
                encoded_jwt = jwt.encode({'user_id':user.id, 'expiration': expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
                return {"status": "success","api_token": encoded_jwt, "packages": [package.as_dict() for package in packages], "userName": user.userName}, 200
            else: return { "status": "Password doesn't match" }

        else:
            return { "status": "No Such User" }
        

    def register(data):
        from modules.packageManagement.models.package import Package
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
        

    
    