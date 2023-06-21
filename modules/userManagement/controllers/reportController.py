from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.userManagement.models.user import User
from modules.bookingManagement.models.booking import Booking
from modules.packageManagement.models.package import Package
from modules import bcrypt, app, db
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
from sqlalchemy import func





class ReportController(Resource):
    def get(self):
        
        # total revenue
        query = db.session.query(Booking, Package).join(Package, Booking.packageId == Package.id)
        query = query.filter(Booking.isCanceled == False)
        total_revenue = float(query.with_entities(func.sum(Package.price)).scalar() or 0)

        # total revenue separately
        custom_package_revenue = db.session.query(db.func.sum(Package.price)).\
            join(Booking, Package.id == Booking.packageId).\
            filter(Booking.isCanceled == False, Package.isCustom == True).scalar()

        non_custom_package_revenue = db.session.query(db.func.sum(Package.price)).\
            join(Booking, Package.id == Booking.packageId).\
            filter(Booking.isCanceled == False, Package.isCustom == False).scalar()

        # each package sold
        query = db.session.query(Booking, Package).join(Package, Booking.packageId == Package.id)
        query = query.filter(Booking.isCanceled == False)
        results = query.group_by(Package.id).with_entities(Package.packageName, func.count(Booking.id), Package.price).all()
        packages_sold = [{"packageName": r[0], "soldCounts": r[1], "packagePrice": float(r[2])} for r in results]

        # sold custom packages count
        custom_packages_sold_count = db.session.query(Booking).\
            join(Package, Booking.packageId == Package.id).\
            filter(Booking.isCanceled == False, Package.isCustom == True).count()

        return { 
            "totalRevenue": total_revenue,
            "customPackageRevenue": float(custom_package_revenue) if custom_package_revenue else 0,
            "preDefinedPackageRevenue": float(non_custom_package_revenue) if non_custom_package_revenue else 0,
            "customPackagesSoldCount": custom_packages_sold_count,
            "preDefinedPackageSoldCount": packages_sold
        }



    def post(self):
        data = request.get_json()
        try:
            decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400
        user = User.query.filter_by(userName=data.get('userName')).first()
        if data["start_date"] is not None:
            start_date = datetime.strptime(data["start_date"], '%Y-%m-%d')
            bookings = Booking.query.filter(Booking.customerId == user.id, Booking.bookingDate >= start_date).all()
            if bookings:
                return { "status": "success", "data": [booking.as_dict() for booking in bookings] }

            else:
                return { "status": "This Customer Has No Booking With That Specific Date" }

        elif data["start_date"] is None:
            bookings = Booking.query.filter(Booking.customerId == user.id).all()
            if bookings:
                return { "status": "success", "data": [booking.as_dict() for booking in bookings] }

            else:
                return { "status": "This Customer Has No Booking" }  
                   
        else: 
            return { "status": "No such user" }    