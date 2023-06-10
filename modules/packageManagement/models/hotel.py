from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event



class Hotel(db.Model):
    __tablename__ = 'hotel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotelName = db.Column(db.String(50), nullable=False)
    cityName = db.Column(db.String(50), nullable=False)
    pricePerNight = db.Column(db.Integer, nullable=False)
    
    def as_dict(self):
        return {c.key: getattr(self, c.key).isoformat() if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key) for c in class_mapper(self.__class__).columns}
