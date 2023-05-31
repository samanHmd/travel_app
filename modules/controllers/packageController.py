from flask import Flask, jsonify
from flask_restful import Api, Resource, fields, marshal_with
from faker import Faker
import random
from datetime import datetime, timedelta
from modules.Models import Flight, Hotel, Activity, Package, PackageHotel, PackageFlight, PackageActivity
from modules import db



flights_data = [
    {"flightNumber": "FL001","departureCity": "Montreal","arrivalCountry": "Italy","arrivalCity": "Rome","departureTime": datetime.strptime('2023-06-10 20:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 700},
    {"flightNumber": "FL002","departureCity": "Montreal","arrivalCountry": "USA","arrivalCity": "Los Angeles","departureTime": datetime.strptime('2023-07-10 10:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 600},
    {"flightNumber": "FL003","departureCity": "Montreal","arrivalCountry": "France","arrivalCity": "Paris","departureTime": datetime.strptime('2023-07-10 10:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 800},
    {"flightNumber": "FL004","departureCity": "Montreal","arrivalCountry": "Germany","arrivalCity": "Berlin","departureTime": datetime.strptime('2023-07-15 10:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 900},
    {"flightNumber": "FL005","departureCity": "Montreal","arrivalCountry": "Spain","arrivalCity": "Madrid","departureTime": datetime.strptime('2023-07-10 10:00:00', '%Y-%m-%d %H:%M:%S'),"flightPrice": 700},
    
]

hotels_data = [
    {"hotelName": "Hotel Rome", "cityName": "Rome", "checkInDate":datetime.strptime('2023-06-21', '%Y-%m-%d'), "checkOutDate": datetime.strptime('2023-06-30', '%Y-%m-%d'), "pricePerNight": 150},
    {"hotelName": "Hotel LA","cityName": "Los Angeles","checkInDate": datetime.strptime('2023-07-16', '%Y-%m-%d'),"checkOutDate": datetime.strptime('2023-07-25', '%Y-%m-%d'),"pricePerNight": 200},
    {"hotelName": "Hotel Paris","cityName": "Paris","checkInDate": datetime.strptime('2023-07-16', '%Y-%m-%d'),"checkOutDate": datetime.strptime('2023-07-25', '%Y-%m-%d'),"pricePerNight": 180},
    {"hotelName": "Hotel Berlin","cityName": "Berlin","checkInDate": datetime.strptime('2023-07-16', '%Y-%m-%d'),"checkOutDate": datetime.strptime('2023-07-25', '%Y-%m-%d'),"pricePerNight": 190},
    {"hotelName": "Hotel Madrid","cityName": "Madrid","checkInDate": datetime.strptime('2023-07-16', '%Y-%m-%d'),"checkOutDate": datetime.strptime('2023-07-25', '%Y-%m-%d'),"pricePerNight": 160},
]

activities_data = [
    {"activityName": "Hiking", "price": 10},
    {"activityName": "Biking", "price": 15},
    {"activityName": "Museum", "price": 20},
    {"activityName": "City Tour", "price": 40},
    {"activityName": "Running around the Hotel", "price": 80},
]

packages_data = [
    {"packageName": "Rome Tour", "daysCount": 5, "flight_id": 1, "hotel_ids": [1], "activity_ids": [1]},
    {"packageName": "LA Tour", "daysCount": 10, "flight_id": 2, "hotel_ids": [2], "activity_ids": [2]},
    {"packageName": "Paris Tour", "daysCount": 6, "flight_id": 2, "hotel_ids": [3], "activity_ids": [3]},
    {"packageName": "Berlin Tour", "daysCount": 3, "flight_id": 2, "hotel_ids": [4], "activity_ids": [4]},
    {"packageName": "Madrid Tour", "daysCount": 4, "flight_id": 2, "hotel_ids": [5], "activity_ids": [5]},
    
]




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
    
        # populate hotels
        for hotel in hotels_data:
            new_hotel = Hotel(**hotel)
            db.session.add(new_hotel)

        # populate activities
        for activity in activities_data:
            new_activity = Activity(**activity)
            db.session.add(new_activity)

        db.session.commit()

        # populate packages
        for package in packages_data:
            new_package = Package(packageName=package["packageName"], daysCount=package["daysCount"])
            db.session.add(new_package)
            db.session.commit()  # commit to get the package id

            # associate flight with package
            new_package_flight = PackageFlight(package_id=new_package.id, flight_id=package["flight_id"])
            db.session.add(new_package_flight)

            # associate hotels with package
            for hotel_id in package["hotel_ids"]:
                new_package_hotel = PackageHotel(package_id=new_package.id, hotel_id=hotel_id)
                db.session.add(new_package_hotel)

            # associate activities with package
            for activity_id in package["activity_ids"]:
                new_package_activity = PackageActivity(package_id=new_package.id, activity_id=activity_id)
                db.session.add(new_package_activity)

        db.session.commit()
        return "success"