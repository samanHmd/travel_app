from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.Models import User, Package
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta


flight_field = {
    'id': fields.Integer,
    'flightNumber': fields.String,
    'departureTime': fields.DateTime,
    'arrivalTime': fields.DateTime,
    'departureLocation': fields.String,
    'arrivalLocation': fields.String,
    'price': fields.String,
}



hotel_field = {
    'id': fields.Integer,
    'hotelName': fields.String,
    'checkInDate': fields.DateTime,
    'checkOutDate': fields.DateTime,
    'location': fields.String,
    'pricePerNight': fields.String,
}



activity_field = {
    'id': fields.Integer,
    'activityName': fields.String,
    'location': fields.String,
    'price': fields.String,
}

package_field = {
    'id': fields.Integer,
    'packageName': fields.String,
    'price': fields.Float,
    'flights': fields.List(fields.Nested(flight_field), attribute=lambda x: x.get_flights()),
    'hotels': fields.List(fields.Nested(hotel_field), attribute=lambda x: x.get_hotels()),
    'activities': fields.List(fields.Nested(activity_field), attribute=lambda x: x.get_activities()),
}

class LoginController(Resource):
    @marshal_with(package_field)
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
            return {"status": "success","api_token": encoded_jwt, "packages": marshal(packages, package_field)}, 200
        else:
            return { "status": "fail" }