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
from modules.userManagement.models.user import User
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl




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
        booking.isCanceled = True
        db.session.commit() 

        user = User.query.get(booking.customerId)

        #Email
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
        message = Mail(
            from_email='travelapplicationconcordia@gmail.com',
            to_emails=user.email,
        )
        message.template_id = 'd-255889ec5c4d48b4bf0c3a1de4e13ed6'  # Replace with your template ID

        message.dynamic_template_data = {
        'name': user.name,
        'ID': booking.id
        }
        try:
            print(os.environ.get('SENDGRID_API_KEY'))
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

        bookings = Booking.query.filter(Booking.isCanceled == False).all()
        return { "status": "Success", "bookings": [booking.as_dict() for booking in bookings] }