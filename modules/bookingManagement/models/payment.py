from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules.bookingManagement.models.booking import Booking


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paymentAmount = db.Column(db.Integer, nullable=False)
    paymentDate = db.Column(db.DateTime, default=datetime.utcnow)
    booking_id =  db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    isSuccess = db.Column(db.Boolean, nullable=False)





with app.app_context():
    db.create_all()   