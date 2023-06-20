from modules import db, app
from datetime import datetime
from flask import Flask, jsonify
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules import bcrypt, app
from datetime import datetime, timedelta
from modules.packageManagement.models.package import Package
import jwt
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
from modules import db, app
from modules.packageManagement.models.package import Package, PackageActivity, PackageFlight, PackageHotel
import stripe

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, userName={self.userName}, email={self.email})"

    def login(data):
        required_fields = ['userName', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            

        user = User.query.filter_by(userName=data.get('userName')).first()
        packages = Package.query.all()
        if user:
            if bcrypt.check_password_hash(user.password, data.get('password')):
                expiration_time = (datetime.utcnow() + timedelta(seconds=172800)).isoformat()
                encoded_jwt = jwt.encode({'user_id':user.id, 'expiration': expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
                return {"status": "success","api_token": encoded_jwt, "packages": [package.as_dict() for package in packages], "userName": user.userName}, 200
            else: return { "status": "Password doesn't match" }

        else:
            return { "status": "No Such User" }
        

    def register(data):
        required_fields = ['userName', 'name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            
        if len(data['password']) < 5:
            return {"error": "Password should be at least 5 characters."}, 400
        
        existing_user_username = User.query.filter_by(userName=data.get('userName')).first()
        existing_user_email = User.query.filter_by(email=data.get('email')).first()

        if existing_user_username or existing_user_email:
            return {'error': 'Username or email already exists.'}, 400
            
        try:
            password = data.get('password')
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=data.get('name'), userName=data.get('userName'), email=data.get('email'), password=hashed)
            db.session.add(user)
            db.session.commit()
            db.session.flush()
        except IntegrityError as ie:
            print("IntegrityError: ", ie) # Let's print the error message
            db.session.rollback()
            return {'error': 'Username or email already exists.'}, 400
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return {'error': str(e)}, 400
        finally:
            user = User.query.filter_by(userName=data.get('userName')).first()
            packages = Package.query.all()
            expiration_time = (datetime.utcnow() + timedelta(seconds=172800)).isoformat()
            encoded_jwt = jwt.encode({'user_id':user.id, 'expiration': expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
            return {"status": "success","api_token": encoded_jwt, "packages": [package.as_dict() for package in packages], "userName": user.userName}, 200
        


    def createCusotmPackage(data):
        required_fields = ['api_token', 'flight_id', 'hotel_ids', 'activity_ids', 'check_in_date', 'check_out_date', 'flightPrice', 'hotelPrice', 'activityPrice']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            
            if field in ["flight_id", "flightPrice"]:
                if not isinstance(data[field], int):
                    return {"error": f"{field} must be an integer."}, 400
            elif field in ["hotel_ids", "activity_ids", "hotelPrice", "activityPrice"]:
                if not isinstance(data[field], list):
                    return {"error": f"{field} must be a list."}, 400
                if not all(isinstance(i, int) for i in data[field]):
                    return {"error": f"All elements in {field} must be integers."}, 400

        try:
            check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
            check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        except ValueError:
            return {"error": "Dates must be in 'YYYY-MM-DD' format."}, 400

        flightPrice = data["flightPrice"]
        hotelPrices = data.get('hotelPrice',[])
        activityPrices = data.get('activityPrice',[])
        daysCount = check_out_date - check_in_date

        try:
            decoded_jwt = jwt.decode(data["api_token"], app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400

        user_id = decoded_jwt["user_id"]
        flightId = data.get("flight_id"),
        flightId = flightId[0]
        hotel_ids = data.get('hotel_ids', [])
        activity_ids = data.get('activity_ids', [])
        totalPrice = 0
        temp = 0
        

        for hotelPrice in hotelPrices:
            temp = temp + hotelPrice

        temp = temp/len(hotelPrices)  
        totalPrice = temp*daysCount.days

        for activityPrice in activityPrices:
            totalPrice = totalPrice + activityPrice

        totalPrice = totalPrice + flightPrice   
        
        new_package = Package(packageName=f"Custom package for user {user_id} on {check_in_date.strftime('%Y-%m-%d')}", daysCount=daysCount, isCustom=True, price=totalPrice)
        db.session.add(new_package)
        db.session.commit()  
        new_package.price = totalPrice
        
        new_package_flight = PackageFlight(packageId=new_package.id, flightId=flightId)
        db.session.add(new_package_flight)

        
        for hotel_id in hotel_ids:
            new_package_hotel = PackageHotel(packageId=new_package.id, hotelId=hotel_id)
            db.session.add(new_package_hotel)

        
        for activity_id in activity_ids:
            new_package_activity = PackageActivity(packageId=new_package.id, activityId=activity_id)
            db.session.add(new_package_activity)

        
        db.session.commit()

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                      'price_data': {
                        'currency': 'usd',
                        'product_data': {
                          'name': 'Custom Package',
                        },
                        'unit_amount': int(totalPrice)*100,
                      },
                      'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                metadata={
                    'customer_id': user_id,
                    'package_id': 1,
                    'departureDate': check_in_date.strftime('%Y-%m-%d'),
                    'returnDate': check_out_date.strftime('%Y-%m-%d'),
                },
            )
            
        except Exception as e:
            return str(e)

        
        return { "status": "success", "url":checkout_session.url}, 200
    


    def getPackages():
        packages = Package.query.all()
        return jsonify([package.as_dict() for package in packages])