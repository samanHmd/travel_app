from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel
from modules.packageManagement.models.activity import Activity
from modules.bookingManagement.models.booking import Booking


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