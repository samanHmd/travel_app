from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, userName={self.userName}, email={self.email})"


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    bookingDate = db.Column(db.DateTime, default=datetime.utcnow)
    departureDate = db.Column(db.DateTime, nullable=False) 
    returnDate = db.Column(db.DateTime, nullable=False)
    def as_dict(self):
        return {c.key: getattr(self, c.key).isoformat() if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key) for c in class_mapper(self.__class__).columns}

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paymentAmount = db.Column(db.Integer, nullable=False)
    paymentDate = db.Column(db.DateTime, default=datetime.utcnow)
    booking_id =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    isSuccess = db.Column(db.Boolean, nullable=False)


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

class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flightNumber = db.Column(db.String(50), nullable=False, unique=True)
    departureCity = db.Column(db.String(50), nullable=False)
    arrivalCountry = db.Column(db.String(50), nullable=False)
    arrivalCity = db.Column(db.String(50), nullable=False)
    departureTime = db.Column(db.DateTime, nullable=False)
    flightPrice = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {c.key: getattr(self, c.key).isoformat() if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key) for c in class_mapper(self.__class__).columns}



class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotelName = db.Column(db.String(50), nullable=False)
    cityName = db.Column(db.String(50), nullable=False)
    pricePerNight = db.Column(db.Integer, nullable=False)
    
    def as_dict(self):
        return {c.key: getattr(self, c.key).isoformat() if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key) for c in class_mapper(self.__class__).columns}


class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activityName = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}

class PackageFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))

class PackageHotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))

class PackageActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))


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





#Add app context here
with app.app_context():
    db.create_all()    
