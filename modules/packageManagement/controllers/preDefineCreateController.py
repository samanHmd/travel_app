from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.userManagement.models.user import User
from modules.packageManagement.models.package import Package, PackageActivity, PackageFlight, PackageHotel
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel
from modules.packageManagement.models.activity import Activity
from modules import bcrypt, app, db
import jwt
from datetime import datetime, timedelta





class PreDefineCreateController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_jwt

    def post(self):
        data = request.get_json()
        
        
        flights = Flight.query.filter(Flight.id.in_(data["flight_ids"])).all()
        hotels = Hotel.query.filter(Hotel.id.in_(data["hotel_ids"])).all()
        activities = Activity.query.filter(Activity.id.in_(data["activity_ids"])).all()

        
        flight_price = sum(flight.flightPrice for flight in flights)
        hotel_price = sum(hotel.pricePerNight for hotel in hotels) * data["daysCount"]
        activity_price = sum(activity.price for activity in activities)

        total_price = flight_price + hotel_price + activity_price

        
        new_package = Package(packageName=data["packageName"], daysCount=data["daysCount"], price=total_price, isCustom=False)
        db.session.add(new_package)
        db.session.commit()  

        
        for flight in flights:
            new_package_flight = PackageFlight(package_id=new_package.id, flight_id=flight.id)
            db.session.add(new_package_flight)

        
        for hotel in hotels:
            new_package_hotel = PackageHotel(package_id=new_package.id, hotel_id=hotel.id)
            db.session.add(new_package_hotel)

        
        for activity in activities:
            new_package_activity = PackageActivity(package_id=new_package.id, activity_id=activity.id)
            db.session.add(new_package_activity)
        new_package.price = new_package.priceCalc
        db.session.commit()


        return {"status": "success"}, 200
        

    def put(self):
        data = request.get_json()

        package_id = data.get('package_id')
        if not package_id:
            return {"error": "package_id is required."}, 400

        package = Package.query.get(package_id)
        if not package:
            return {"error": "No package found with the provided id."}, 404

        
        packageName = data.get('packageName')
        daysCount = data.get('daysCount')
        isCustom = data.get('isCustom')
        flight_ids = data.get('flight_ids')
        hotel_ids = data.get('hotel_ids')
        activity_ids = data.get('activity_ids')

        
        if packageName:
            package.packageName = packageName
        if daysCount is not None:   
            package.daysCount = daysCount
        if isCustom is not None:   
            package.isCustom = isCustom

        
        if flight_ids:
            flights = Flight.query.filter(Flight.id.in_(flight_ids)).all()
            package.flights = flights
        if hotel_ids:
            hotels = Hotel.query.filter(Hotel.id.in_(hotel_ids)).all()
            package.hotels = hotels
        if activity_ids:
            activities = Activity.query.filter(Activity.id.in_(activity_ids)).all()
            package.activities = activities

        package.price = package.priceCalc

        db.session.commit()

        return {"status": "success", "data": package.as_dict()}, 200    