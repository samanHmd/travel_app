from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, userName={self.userName}, email={self.email})"


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    bookingDate = db.Column(db.DateTime, default=datetime.utcnow)

class Package(db.Model):
    __tablename__ = 'package'

    id = db.Column(db.Integer, primary_key=True)
    packageName = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    daysCount = db.Column(db.Integer, nullable=True)
    flights = db.relationship('Flight', secondary='package_flight')
    hotels = db.relationship('Hotel', secondary='package_hotel')
    activities = db.relationship('Activity', secondary='package_activity')
    @property
    def price(self):
        total_price = 0
        for flight in self.flights:
            total_price += flight.flightPrice
        for hotel in self.hotels:
            total_price += hotel.pricePerNight
        for activity in self.activities:
            total_price += activity.price
        return total_price
    
    def as_dict(self):
        dict_repr = {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}
        dict_repr['flights'] = [flight.as_dict() for flight in self.flights]
        dict_repr['hotels'] = [hotel.as_dict() for hotel in self.hotels]
        dict_repr['activities'] = [activity.as_dict() for activity in self.activities]
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
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}



class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotelName = db.Column(db.String(50), nullable=False)
    cityName = db.Column(db.String(50), nullable=False)
    checkInDate = db.Column(db.DateTime, nullable=False) 
    checkOutDate = db.Column(db.DateTime, nullable=False)  
    pricePerNight = db.Column(db.Integer, nullable=False)
    priceTotal = db.Column(db.Integer, nullable=True)

    @property
    def totalPrice(self):
        duration = self.checkOutDate - self.checkInDate
        num_nights = duration.days

        priceTotal = num_nights * self.pricePerNight

        return priceTotal
    
    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in class_mapper(self.__class__).columns}


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


#Add app context here
#with app.app_context():
#    db.create_all()    