from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.Models import User, Booking
from modules import bcrypt, app, db
import jwt
from datetime import datetime, timedelta
import stripe
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'




class BookingController(Resource):
    def get(self):

        return "Bookign Controller get"

    def post(self):
        data = request.get_json()
        encoded_jwt = jwt.decode(data["api_token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = encoded_jwt["user_id"]
        check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
        check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                      'price_data': {
                        'currency': 'usd',
                        'product_data': {
                          'name': 'Custom Package',
                        },
                        'unit_amount':  data["total_price"],
                      },
                      'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                metadata={
                    'customer_id': user_id,
                    'package_id': 1,
                    'departureDate': check_in_date.strftime('%Y-%m-%d'),
                    'returnDate': check_out_date.strftime('%Y-%m-%d'),
                },
            )
            
        except Exception as e:
            return str(e)


        return { "status": "success", "url":checkout_session.url}, 200