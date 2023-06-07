from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.Models import User, Package, Booking
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta





class ReportController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return "success"

    def post(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        user = User.query.filter_by(userName=data.get('userName')).first()
        if data["start_date"] is not None:
            start_date = datetime.strptime(data["start_date"], '%Y-%m-%d')
            bookings = Booking.query.filter(Booking.customer_id == user.id, Booking.bookingDate >= start_date).all()
            if bookings:
                return { "status": "success", "data": [booking.as_dict() for booking in bookings] }

            else:
                return { "status": "This Customer Has No Booking With That Specific Date" }

        elif data["start_date"] is None:
            bookings = Booking.query.filter(Booking.customer_id == user.id).all()
            if bookings:
                return { "status": "success", "data": [booking.as_dict() for booking in bookings] }

            else:
                return { "status": "This Customer Has No Booking" }  
                   
        else: 
            return { "status": "No such user" }    