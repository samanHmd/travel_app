from flask import Flask, jsonify
from flask_restful import Resource, request
from faker import Faker
import random
from datetime import datetime, timedelta
from modules.userManagement.models.user import User
from modules.packageManagement.models.package import Package, PackageHotel, PackageFlight, PackageActivity
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel 
from modules.packageManagement.models.activity import Activity
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
        getPackages_response = User.getPackages();
        return getPackages_response;
        
        

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

            
            new_package_flight = PackageFlight(packageId=new_package.id, flightId=package["flightId"])
            db.session.add(new_package_flight)

            
            for hotel_id in package["hotel_ids"]:
                new_package_hotel = PackageHotel(packageId=new_package.id, hotelId=hotel_id)
                db.session.add(new_package_hotel)

            
            for activity_id in package["activity_ids"]:
                new_package_activity = PackageActivity(packageId=new_package.id, activityId=activity_id)
                db.session.add(new_package_activity)

            new_package.price = new_package.priceCalc
 

        db.session.commit()
        return "success"
    
    def delete(self):
        data = request.get_json()
        packageId = data.get('packageId')

        package = Package.query.get(packageId)

        if package:
            db.session.delete(package)
            db.session.commit()
            packages = Package.query.all()
            return {"status": "success", "message": f"Package with id {packageId} has been deleted.", "packages": [package.as_dict() for package in packages]}, 200
        else:
            return {"status": "error", "message": f"No package found with id {packageId}."}, 404
    
    