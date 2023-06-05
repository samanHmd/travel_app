from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import Booking, Payment
import jwt
from datetime import datetime, timedelta
from modules import db, app
import stripe



class PaymentReturnController(Resource):
    def get(self):
        
        return "create custom get"

    def post(self):
        data = request.get_json()
        status = data['status']
        session = stripe.checkout.Session.retrieve(data['session_id'])
        total_amount = session.amount_total 
        customer_id = session.metadata.get('customer_id')
        package_id = session.metadata.get('package_id')
        departure_date = datetime.strptime(session.metadata.get('departureDate'), '%Y-%m-%d')
        return_date = datetime.strptime(session.metadata.get('returnDate'), '%Y-%m-%d')

        
        new_booking = Booking(customer_id=customer_id, package_id=package_id, departureDate=departure_date, returnDate = return_date )
        db.session.add(new_booking)
        db.session.commit()  

        

        if status == 'success':
            
            new_payment = Payment(paymentAmount=total_amount, booking_id=new_booking.id, isSuccess = True )
            db.session.add(new_payment)
            db.session.commit()  
        elif status == 'fail':
            
            new_payment = Payment(paymentAmount=total_amount, booking_id=new_booking.id, isSuccess = False )
            db.session.add(new_payment)
            db.session.commit()  
            

        return { "status": "success", "test":status}, 200
            