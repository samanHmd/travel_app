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

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'




class BookingController(Resource):
    def get(self):

        return "Bookign Controller get"

    def post(self):
        data = request.get_json()

        required_fields = ['api_token', 'package_id', 'check_in_date', 'check_out_date', 'total_price']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            if field in ["package_id", "total_price"]:
                if not isinstance(data[field], int):
                    return {"error": f"{field} must be an integer."}, 400

        try:
            decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400
        
        user_id = decoded_jwt["user_id"]

        try:
            check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
            check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        except ValueError:
            return {"error": "Dates must be in 'YYYY-MM-DD' format."}, 400


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
                    'package_id': data["package_id"],
                    'departureDate': check_in_date.strftime('%Y-%m-%d'),
                    'returnDate': check_out_date.strftime('%Y-%m-%d'),
                },
            )
            
        except Exception as e:
            return str(e)


        return { "status": "success", "url":checkout_session.url}, 200