from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.packageManagement.models.package import Package, PackageActivity, PackageFlight, PackageHotel
from modules.userManagement.models.user import User
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
from modules import db, app
import stripe

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'


class CreatePackageController(Resource):
    def get(self):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                      'price_data': {
                        'currency': 'usd',
                        'product_data': {
                          'name': 'Custom Package',
                        },
                        'unit_amount': 50,
                      },
                      'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success.html?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel.html?session_id={CHECKOUT_SESSION_ID}',
            )
        except Exception as e:
            return str(e)
        print(checkout_session.url)
        return "create custom get"

    def post(self):
        data = request.get_json()
        createCustomPackage_response = User.createCusotmPackage(data)
        return createCustomPackage_response

        
            