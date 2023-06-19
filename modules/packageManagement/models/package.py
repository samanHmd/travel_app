from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel
from modules.packageManagement.models.activity import Activity



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
        for hotel in self.hotels:
            price += hotel.pricePerNight*self.daysCount
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