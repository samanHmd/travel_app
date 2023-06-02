from flask import Flask, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import User, Package, PackageActivity, PackageFlight, PackageHotel
import jwt
from datetime import datetime, timedelta
from modules import db, app


class CreatePackageController(Resource):
    def get(self):
        return "create custom get"

    def post(self):
        data = request.get_json()
        check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
        check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        encoded_jwt = jwt.decode(data["api_token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = encoded_jwt["user_id"]
        flight_id = data.get("flight_id", [])[0],
        flight_id = flight_id[0]
        hotel_ids = data.get('hotel_ids', [])
        activity_ids = data.get('activity_ids', [])

        # Create the new package
        new_package = Package(packageName=f"Custom package for user {user_id} on {check_in_date.strftime('%Y-%m-%d')}", daysCount=None, isCustom=True)
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


        
        return { "status": "success"}, 200
            