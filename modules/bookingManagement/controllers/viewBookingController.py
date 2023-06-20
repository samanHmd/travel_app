from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.bookingManagement.models.booking import  Booking
from modules import bcrypt, app
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta





class ViewBookingController(Resource):
    def get(self):
        bookings = Booking.query.filter(Booking.isCanceled == False).all()
        return {"status": "success", "bookings": [booking.as_dict() for booking in bookings]}, 200

    def post(self):
        data = request.get_json()
        viewBooking_response = Booking.viewBooking(data)
        return viewBooking_response
