from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.Models import User, Package, Booking
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta





class ViewBookingController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return "success"

    def post(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        booking = Booking.query.get(decoded_jwt["user_id"])
        if booking:
            return { "status": "success", "data": booking.as_dict() }

        else:
            return { "status": "This Costumer Has No Booking" }