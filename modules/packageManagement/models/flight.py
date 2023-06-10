from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event



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

