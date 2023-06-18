from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.bookingManagement.models.booking import  Booking
from modules import bcrypt, app
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta





class ViewPaymentController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return "success"

    def post(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        print(decoded_jwt["user_id"])
        return decoded_jwt
