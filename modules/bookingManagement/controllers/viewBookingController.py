from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.bookingManagement.models.booking import  Booking
from modules import bcrypt, app
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta





class ViewBookingController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return "success"

    def post(self):
        data = request.get_json()

        required_fields = ['api_token']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400

        try:
            decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400
        
        
        booking = Booking.query.get(decoded_jwt["user_id"])
        if booking:
            return { "status": "success", "data": booking.as_dict() }

        else:
            return { "status": "This Costumer Has No Booking" }