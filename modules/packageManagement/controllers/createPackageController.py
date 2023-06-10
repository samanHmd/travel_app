from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.packageManagement.models.package import Package, PackageActivity, PackageFlight, PackageHotel
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

        required_fields = ['api_token', 'flight_id', 'hotel_ids', 'activity_ids', 'check_in_date', 'check_out_date', 'flightPrice', 'hotelPrice', 'activityPrice']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            
            if field in ["flight_id", "flightPrice"]:
                if not isinstance(data[field], int):
                    return {"error": f"{field} must be an integer."}, 400
            elif field in ["hotel_ids", "activity_ids", "hotelPrice", "activityPrice"]:
                if not isinstance(data[field], list):
                    return {"error": f"{field} must be a list."}, 400
                if not all(isinstance(i, int) for i in data[field]):
                    return {"error": f"All elements in {field} must be integers."}, 400

        try:
            check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
            check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        except ValueError:
            return {"error": "Dates must be in 'YYYY-MM-DD' format."}, 400

        flightPrice = data["flightPrice"]
        hotelPrices = data.get('hotelPrice',[])
        activityPrices = data.get('activityPrice',[])
        daysCount = check_out_date - check_in_date

        try:
            decoded_jwt = jwt.decode(data["api_token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400

        user_id = decoded_jwt["user_id"]
        flight_id = data.get("flight_id"),
        flight_id = flight_id[0]
        hotel_ids = data.get('hotel_ids', [])
        activity_ids = data.get('activity_ids', [])
        totalPrice = 0
        temp = 0
        

        for hotelPrice in hotelPrices:
            temp = temp + hotelPrice

        temp = temp/len(hotelPrices)  
        totalPrice = temp*daysCount.days

        for activityPrice in activityPrices:
            totalPrice = totalPrice + activityPrice

        totalPrice = totalPrice + flightPrice   
        
        new_package = Package(packageName=f"Custom package for user {user_id} on {check_in_date.strftime('%Y-%m-%d')}", daysCount=daysCount, isCustom=True)
        db.session.add(new_package)
        db.session.commit()  
        new_package.price = totalPrice
        
        new_package_flight = PackageFlight(package_id=new_package.id, flight_id=flight_id)
        db.session.add(new_package_flight)

        
        for hotel_id in hotel_ids:
            new_package_hotel = PackageHotel(package_id=new_package.id, hotel_id=hotel_id)
            db.session.add(new_package_hotel)

        
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
                        'unit_amount': int(totalPrice),
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
            