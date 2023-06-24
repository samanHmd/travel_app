from modules import db, app
from datetime import datetime
from flask import Flask, jsonify
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel
from modules.packageManagement.models.activity import Activity
from sqlalchemy import inspect
import logging
import jwt
from jwt import InvalidTokenError
import stripe
from modules.data import flights_data, hotels_data, activities_data, packages_data


stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'

class Package(db.Model):
    __tablename__ = 'package'

    id = db.Column(db.Integer, primary_key=True)
    packageName = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    daysCount = db.Column(db.Integer, nullable=True)
    isCustom = db.Column(db.Boolean, nullable=False)
    flights = db.relationship('Flight', secondary='package_flight')
    hotels = db.relationship('Hotel', secondary='package_hotel')
    activities = db.relationship('Activity', secondary='package_activity')
    @property
    def priceCalc(self):
        price = 0
        for flight in self.flights:
            price += flight.flightPrice
        if self.hotels:
            average_hotel_price = sum(hotel.pricePerNight for hotel in self.hotels) / len(self.hotels)
            price += average_hotel_price * self.daysCount
        for activity in self.activities:
            price += activity.price
        return price
    
    def as_dict(self):
        def convert_datetime(value):
            if isinstance(value, datetime):
                return value.isoformat()
            return value

        dict_repr = {c.key: convert_datetime(getattr(self, c.key)) for c in class_mapper(self.__class__).columns}

        dict_repr['flights'] = [dict((key, convert_datetime(value)) for key, value in flight.as_dict().items()) for flight in self.flights]
        dict_repr['hotels'] = [dict((key, convert_datetime(value)) for key, value in hotel.as_dict().items()) for hotel in self.hotels]
        dict_repr['activities'] = [dict((key, convert_datetime(value)) for key, value in activity.as_dict().items()) for activity in self.activities]
    
        return dict_repr
    

    def createPreDefineSamples(self):
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


    def createPreDefine(data):
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
            new_package_flight = PackageFlight(packageId=new_package.id, flightId=flight.id)
            db.session.add(new_package_flight)

        
        for hotel in hotels:
            new_package_hotel = PackageHotel(packageId=new_package.id, hotelId=hotel.id)
            db.session.add(new_package_hotel)

        
        for activity in activities:
            new_package_activity = PackageActivity(packageId=new_package.id, activityId=activity.id)
            db.session.add(new_package_activity)
        new_package.price = new_package.priceCalc
        db.session.commit()
        return {"status": "success"}, 200

    def preDefineUpdate(data):
        packageId = data.get('package_id')
        if not packageId:
            return {"error": "package_id is required."}, 400

        package = Package.query.get(packageId)
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

    def preDefineDelete(data):
        from modules.bookingManagement.models.booking import Booking
        packageId = data.get('packageId')
        package = Package.query.get(packageId)
        if package:
            booking = Booking.query.filter_by(packageId=packageId).first()
            if booking:
                return {"status": "error", "message": "There is a booking for this package. It cannot be deleted."}, 400
            else:
                db.session.delete(package)
                db.session.commit()
                packages = Package.query.all()
                return {"status": "success", "message": "Package has been deleted.", "packages": [package.as_dict() for package in packages]}, 200
        else:
            return {"status": "error", "message": "No package found with this id"}, 404


    
    def update_package_price(package_id):
        # Get the package
        package = Package.query.get(package_id)
    
        # Calculate the price
        totalPrice = 0
        temp = 0
    
        if package.hotels:
            average_hotel_price = sum(hotel.pricePerNight for hotel in package.hotels) / len(package.hotels)
            totalPrice += average_hotel_price * package.daysCount
    
        for activity in package.activities:
            totalPrice += activity.price
    
        for flight in package.flights:
            totalPrice += flight.flightPrice
    
        # Update the package price
        package.price = totalPrice
        db.session.commit()



    def createCusotmPackage(data):
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
        flightId = data.get("flight_id")
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
        new_package = Package(packageName="Custom Package", daysCount=daysCount.days, isCustom=True, price=totalPrice)
        db.session.add(new_package)
        db.session.commit()
        
        
        
        new_package_flight = PackageFlight(packageId=new_package.id, flightId=flightId)
        db.session.add(new_package_flight)
        
        Package.update_package_price(new_package.id)

        for hotel_id in hotel_ids:
            new_package_hotel = PackageHotel(packageId=new_package.id, hotelId=hotel_id)
            db.session.add(new_package_hotel)

        Package.update_package_price(new_package.id)
        
        for activity_id in activity_ids:
            new_package_activity = PackageActivity(packageId=new_package.id, activityId=activity_id)
            db.session.add(new_package_activity)

        Package.update_package_price(new_package.id)
        
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
                        'unit_amount': int(totalPrice)*100,
                      },
                      'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                metadata={
                    'customer_id': user_id,
                    'package_id': new_package.id,
                    'departureDate': check_in_date.strftime('%Y-%m-%d'),
                    'returnDate': check_out_date.strftime('%Y-%m-%d'),
                },
            )
            
        except Exception as e:
            return str(e)

        db.session.close()
        return { "status": "success", "url":checkout_session.url}, 200



    def getPackages():
        packages = Package.query.all()
        return jsonify([package.as_dict() for package in packages])



    def returnComponents(data):
        required_fields = ['departureCity', 'destinationCity', 'check_in_date', 'check_out_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400

        try:
            check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
            check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        except ValueError:
            return {"error": "Dates must be in 'YYYY-MM-DD' format."}, 400

        flights = Flight.query.filter_by(departureCity= data.get('departureCity'), arrivalCity=data.get('destinationCity')).all()
        hotels = Hotel.query.filter_by(cityName=data.get('destinationCity')).all()
        activities = Activity.query.all()
        print(flights)
        return {
            "status": "success",
            "flights": [flight.as_dict() for flight in flights],
            "hotels": [hotel.as_dict() for hotel in hotels],
            "activities": [activity.as_dict() for activity in activities]
            }, 200




class PackageFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    packageId = db.Column(db.Integer, db.ForeignKey('package.id'))
    flightId = db.Column(db.Integer, db.ForeignKey('flight.id'))

class PackageHotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    packageId = db.Column(db.Integer, db.ForeignKey('package.id'))
    hotelId = db.Column(db.Integer, db.ForeignKey('hotel.id'))

class PackageActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    packageId = db.Column(db.Integer, db.ForeignKey('package.id'))
    activityId = db.Column(db.Integer, db.ForeignKey('activity.id'))


# @event.listens_for(Hotel, 'before_insert')
# @event.listens_for(Hotel, 'before_update')
# def receive_before_insert(mapper, connection, hotel):
#     hotel.priceTotal = hotel.totalPrice

@event.listens_for(Package, 'before_insert')
@event.listens_for(Package, 'before_update')
def receive_before_insert(mapper, connection, package):
    package.price = package.priceCalc

@event.listens_for(Package.flights, 'append')
@event.listens_for(Package.flights, 'remove')
def update_package_on_flights_change(package, flight, initiator):
    package.price = package.priceCalc

@event.listens_for(Package.hotels, 'append')
@event.listens_for(Package.hotels, 'remove')
def update_package_on_hotels_change(package, hotel, initiator):
    package.price = package.priceCalc

@event.listens_for(Package.activities, 'append')
@event.listens_for(Package.activities, 'remove')
def update_package_on_activities_change(package, activity, initiator):
    package.price = package.priceCalc    



with app.app_context():
    db.create_all()     