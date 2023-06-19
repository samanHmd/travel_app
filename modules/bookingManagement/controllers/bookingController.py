from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules import bcrypt, app, db
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
import stripe
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
from modules.bookingManagement.models.booking import Booking






class BookingController(Resource):
    def get(self):

        return "Bookign Controller get"

    def post(self):
        data = request.get_json()
        booking_response = Booking.booking(data)
        return booking_response
    

    def put(self):
        return "success"
    
    def delete(self):
        data = request.get_json()
        
        booking = Booking.query.get(data['bookingId'])
        
        print(booking)
        return "success"