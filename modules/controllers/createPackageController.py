from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import User, Package, PackageActivity, PackageFlight, PackageHotel
import jwt
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
            # session = stripe.checkout.Session.retrieve(session_id)
            # total_amount = session.amount_total 
        except Exception as e:
            return str(e)
        print(checkout_session.url)
        return "create custom get"

    def post(self):
        data = request.get_json()
        flightPrice = data["flightPrice"]
        hotelPrice = data["hotelPrice"]
        activityPrice = data["activityPrice"]
        check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
        check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        daysCount = check_out_date - check_in_date
        encoded_jwt = jwt.decode(data["api_token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = encoded_jwt["user_id"]
        flight_id = data.get("flight_id", [])[0],
        flight_id = flight_id[0]
        hotel_ids = data.get('hotel_ids', [])
        activity_ids = data.get('activity_ids', [])

        

        # Create the new package
        new_package = Package(packageName=f"Custom package for user {user_id} on {check_in_date.strftime('%Y-%m-%d')}", daysCount=daysCount, isCustom=True)
        db.session.add(new_package)
        db.session.commit()  # commit to get the package id

        # Associate flight with package
        new_package_flight = PackageFlight(package_id=new_package.id, flight_id=flight_id)
        db.session.add(new_package_flight)

        # Associate hotels with package
        for hotel_id in hotel_ids:
            new_package_hotel = PackageHotel(package_id=new_package.id, hotel_id=hotel_id)
            db.session.add(new_package_hotel)

        # Associate activities with package
        for activity_id in activity_ids:
            new_package_activity = PackageActivity(package_id=new_package.id, activity_id=activity_id)
            db.session.add(new_package_activity)

        db.session.commit()

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
            