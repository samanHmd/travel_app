from modules import db, app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, userName={self.userName}, email={self.email}, password={self.password})"

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer = db.Column(db.String, nullable=False)
    package = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Integer, nullable=False)
    costumer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Package(db.Model):
    __tablename__ = 'package'

    id = db.Column(db.Integer, primary_key=True)
    packageName = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    daysCount = db.Column(db.Integer, nullable=True)
    components = db.relationship('PackageComponent', backref='package', lazy=True)

    def get_flights(self):
        return Flight.query.join(PackageComponent).filter_by(package_id=self.id, componentType='flight').all()

    def get_hotels(self):
        return Hotel.query.join(PackageComponent).filter_by(package_id=self.id, componentType='hotel').all()

    def get_activities(self):
        return Activity.query.join(PackageComponent).filter_by(package_id=self.id, componentType='activity').all()


class Flight(db.Model):
    __tablename__ = 'flight'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flightNumber = db.Column(db.String(50), nullable=False)
    departureLocation = db.Column(db.String(50), nullable=False)
    arrivalCountry = db.Column(db.String(50), nullable=False)
    arrivalCity = db.Column(db.String(50), nullable=False)
    departureTime = db.Column(db.DateTime, nullable=False)
    arrivalTime = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    package_component = db.relationship('PackageComponent', backref='flight', uselist=False)

class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotelName = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    checkInDate = db.Column(db.DateTime, nullable=False)  # add this
    checkOutDate = db.Column(db.DateTime, nullable=False)  # and this
    pricePerNight = db.Column(db.Float, nullable=False)
    package_component = db.relationship('PackageComponent', backref='hotel', uselist=False)

class Activity(db.Model):
    __tablename__ = 'activity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activityName = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    package_component = db.relationship('PackageComponent', backref='activity', uselist=False)

class PackageComponent(db.Model):
    __tablename__ = 'package_component'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    componentType = db.Column(db.String(50), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))



#Add app context here
with app.app_context():
    db.create_all()    