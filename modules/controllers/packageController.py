from flask import Flask, jsonify
from flask_restful import Api, Resource, fields, marshal_with
from faker import Faker
import random
from datetime import datetime, timedelta
from modules.Models import Flight, Hotel, Activity, Package, PackageComponent
from modules import db

faker = Faker()

flight_field = {
    'id': fields.Integer,
    'flightNumber': fields.String,
    'departureTime': fields.DateTime,
    'arrivalTime': fields.DateTime,
    'departureLocation': fields.String,
    'arrivalLocation': fields.String,
    'price': fields.String,
}



hotel_field = {
    'id': fields.Integer,
    'hotelName': fields.String,
    'checkInDate': fields.DateTime,
    'checkOutDate': fields.DateTime,
    'location': fields.String,
    'pricePerNight': fields.String,
}



activity_field = {
    'id': fields.Integer,
    'activityName': fields.String,
    'location': fields.String,
    'price': fields.String,
}

package_field = {
    'id': fields.Integer,
    'packageName': fields.String,
    'price': fields.Float,
    'flights': fields.List(fields.Nested(flight_field), attribute=lambda x: x.get_flights()),
    'hotels': fields.List(fields.Nested(hotel_field), attribute=lambda x: x.get_hotels()),
    'activities': fields.List(fields.Nested(activity_field), attribute=lambda x: x.get_activities()),
}

class PackageController(Resource):
    @marshal_with(package_field)
    def get(self):
        packages = Package.query.all()
        #db.drop_all()
        #db.create_all()
        return packages
        

    def post(self):
        for _ in range(10):
            start_date = datetime.now()
            end_date = start_date + timedelta(days=10)

            flight = Flight(
                flightNumber=faker.unique.bothify(text='??###'),
                departureLocation=faker.city(),
                arrivalCountry=faker.city(),
                arrivalCity=faker.city(),
                departureTime=faker.date_time_between_dates(datetime_start=start_date, datetime_end=end_date),
                arrivalTime=faker.date_time_between_dates(datetime_start=start_date, datetime_end=end_date),
                price=random.uniform(100.0, 1000.0)
            )

            hotel = Hotel(
                hotelName=faker.company(),
                location=faker.city(),
                checkInDate=faker.date_time_between_dates(datetime_start=start_date, datetime_end=end_date),
                checkOutDate=faker.date_time_between_dates(datetime_start=start_date, datetime_end=end_date),
                pricePerNight=random.uniform(50.0, 300.0)
            )

            activity = Activity(
                activityName=faker.bs(),
                location=faker.city(),
                price=random.uniform(20.0, 200.0)
            )

            db.session.add(flight)
            db.session.add(hotel)
            db.session.add(activity)
            db.session.commit()

            package = Package(
                packageName=faker.catch_phrase(),
                price=flight.price + hotel.pricePerNight + activity.price
            )

            db.session.add(package)
            db.session.commit()

            flight_component = PackageComponent(
                componentType='flight',
                package_id=package.id,
                flight_id=flight.id
            )

            hotel_component = PackageComponent(
                componentType='hotel',
                package_id=package.id,
                hotel_id=hotel.id
            )

            activity_component = PackageComponent(
                componentType='activity',
                package_id=package.id,
                activity_id=activity.id
            )

            db.session.add(flight_component)
            db.session.add(hotel_component)
            db.session.add(activity_component)
            db.session.commit()

        return "packages post success"