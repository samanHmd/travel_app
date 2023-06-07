from flask import Flask, jsonify
from flask_restful import Api, Resource, fields, marshal_with
from faker import Faker
import random
from datetime import datetime, timedelta
from modules.Models import Flight, Hotel, Activity, Package, PackageHotel, PackageFlight, PackageActivity
from modules import db
from modules.data import flights_data, hotels_data, activities_data, packages_data






# flight_field = {
#     'id': fields.Integer,
#     'flightNumber': fields.String,
#     'departureTime': fields.DateTime,
#     'arrivalTime': fields.DateTime,
#     'departureLocation': fields.String,
#     'arrivalCountry': fields.String,
#     'arrivalCity': fields.String,
#     'price': fields.String,
# }



# hotel_field = {
#     'id': fields.Integer,
#     'hotelName': fields.String,
#     'checkInDate': fields.DateTime,
#     'checkOutDate': fields.DateTime,
#     'location': fields.String,
#     'pricePerNight': fields.String,
# }



# activity_field = {
#     'id': fields.Integer,
#     'activityName': fields.String,
#     'location': fields.String,
#     'price': fields.String,
# }

# package_field = {
#     'id': fields.Integer,
#     'packageName': fields.String,
#     'price': fields.Float,
#     'flights': fields.List(fields.Nested(flight_field), attribute=lambda x: x.get_flights()),
#     'hotels': fields.List(fields.Nested(hotel_field), attribute=lambda x: x.get_hotels()),
#     'activities': fields.List(fields.Nested(activity_field), attribute=lambda x: x.get_activities()),
# }

class PackageController(Resource):
    #@marshal_with(package_field)
    def get(self):
        packages = Package.query.all()
        return jsonify([package.as_dict() for package in packages])
        

    def post(self):
        for flight in flights_data:
            new_flight = Flight(**flight)
            db.session.add(new_flight)
    
        
        for hotel in hotels_data:
            new_hotel = Hotel(**hotel)
            db.session.add(new_hotel)

        
        for activity in activities_data:
            new_activity = Activity(**activity)
            db.session.add(new_activity)

        db.session.commit()

        
        for package in packages_data:
            new_package = Package(packageName=package["packageName"], daysCount=package["daysCount"], isCustom=False)
            db.session.add(new_package)
            db.session.commit()  

            
            new_package_flight = PackageFlight(package_id=new_package.id, flight_id=package["flight_id"])
            db.session.add(new_package_flight)

            
            for hotel_id in package["hotel_ids"]:
                new_package_hotel = PackageHotel(package_id=new_package.id, hotel_id=hotel_id)
                db.session.add(new_package_hotel)

            
            for activity_id in package["activity_ids"]:
                new_package_activity = PackageActivity(package_id=new_package.id, activity_id=activity_id)
                db.session.add(new_package_activity)

            new_package.price = new_package.priceCalc
 

        db.session.commit()
        return "success"
    
    