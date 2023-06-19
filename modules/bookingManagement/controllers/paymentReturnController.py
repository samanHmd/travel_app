from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.bookingManagement.models.booking import Booking
from modules.bookingManagement.models.payment import Payment
from modules.userManagement.models.user import User
import jwt
from datetime import datetime, timedelta
from modules import db, app
import stripe
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl


class PaymentReturnController(Resource):
    def get(self):
        
        return "create custom get"

    def post(self):
        data = request.get_json()

        required_fields = ['status', 'session_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            
        status = data['status']
        session = stripe.checkout.Session.retrieve(data['session_id'])
        total_amount = session.amount_total 
        customerId = session.metadata.get('customerId')
        packageId = session.metadata.get('package_id')
        departure_date = datetime.strptime(session.metadata.get('departureDate'), '%Y-%m-%d')
        return_date = datetime.strptime(session.metadata.get('returnDate'), '%Y-%m-%d')

        
        new_booking = Booking(customerId=customerId, packageId=packageId, departureDate=departure_date, returnDate = return_date, isCanceled = False )
        db.session.add(new_booking)
        db.session.commit()  

        user = User.query.get(customerId)

        #Email
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
        message = Mail(
            from_email='travelapplicationconcordia@gmail.com',
            to_emails=user.email,
        )
        message.template_id = 'd-3f55eb477da64e6f943fbe47a69b4fb8'  # Replace with your template ID

        message.dynamic_template_data = {
        'name': user.name,
        'ID': new_booking.id
        }
        try:
            print(os.environ.get('SENDGRID_API_KEY'))
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        if status == 'success':
            
            new_payment = Payment(paymentAmount=total_amount, bookingId=new_booking.id, isSuccess = True )
            db.session.add(new_payment)
            db.session.commit()  
        elif status == 'fail':
            
            new_payment = Payment(paymentAmount=total_amount, bookingId=new_booking.id, isSuccess = False )
            db.session.add(new_payment)
            db.session.commit()  
            

        return { "status": "success", "test":status}, 200
            