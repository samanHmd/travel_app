from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    bookingDate = db.Column(db.DateTime, default=datetime.utcnow)
    departureDate = db.Column(db.DateTime, nullable=False) 
    returnDate = db.Column(db.DateTime, nullable=False)
    def as_dict(self):
        return {c.key: getattr(self, c.key).isoformat() if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key) for c in class_mapper(self.__class__).columns}