from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from modules import bcrypt, app, db
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
import stripe
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ssl
from sqlalchemy import event
stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customerId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    packageId = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    bookingDate = db.Column(db.DateTime, default=datetime.utcnow)
    departureDate = db.Column(db.DateTime, nullable=False) 
    returnDate = db.Column(db.DateTime, nullable=False)
    isCanceled = db.Column(db.Boolean, nullable=False)
    def as_dict(self):
        return {c.key: getattr(self, c.key).isoformat() if isinstance(getattr(self, c.key), datetime) else getattr(self, c.key) for c in class_mapper(self.__class__).columns}
    

    def booking(data):
        required_fields = ['api_token', 'package_id', 'check_in_date', 'check_out_date', 'total_price']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            if field in ["package_id", "total_price"]:
                if not isinstance(data[field], int):
                    return {"error": f"{field} must be an integer."}, 400

        try:
            decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400
        
        user_id = decoded_jwt["user_id"]

        try:
            check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
            check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        except ValueError:
            return {"error": "Dates must be in 'YYYY-MM-DD' format."}, 400


        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                      'price_data': {
                        'currency': 'usd',
                        'product_data': {
                          'name': 'Custom Package',
                        },
                        'unit_amount':  data["total_price"],
                      },
                      'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                metadata={
                    'customer_id': user_id,
                    'package_id': data["package_id"],
                    'departureDate': check_in_date.strftime('%Y-%m-%d'),
                    'returnDate': check_out_date.strftime('%Y-%m-%d'),
                },
            )
            
        except Exception as e:
            return str(e)


        return { "status": "success", "url":checkout_session.url}, 200
    



    def viewBooking(data):
        required_fields = ['api_token']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400

        try:
            decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        except InvalidTokenError:
            return {"error": "Invalid api token."}, 400
        
        
        booking = Booking.query.get(decoded_jwt["user_id"])
        if booking:
            return { "status": "success", "data": booking.as_dict() }

        else:
            return { "status": "This Costumer Has No Booking" }
        

    
    def cancelBooking(data):
        booking = Booking.query.get(data['bookingId'])
        booking.isCanceled = True
        db.session.commit() 
        from modules.userManagement.models.user import User
        user = User.query.get(booking.customerId)

        print(user.email)
        print(user.name)
        #Email
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
            getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
        message = Mail(
            from_email='travelapplicationconcordia@gmail.com',
            to_emails=user.email,
        )
        message.template_id = 'd-255889ec5c4d48b4bf0c3a1de4e13ed6'  # Replace with your template ID

        message.dynamic_template_data = {
        'name': user.name,
        'ID': booking.id
        }
        try:
            print(os.environ.get('SENDGRID_API_KEY'))
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

        bookings = Booking.query.filter(Booking.isCanceled == False).all()
        return { "status": "Success", "bookings": [booking.as_dict() for booking in bookings] }




with app.app_context():
    db.create_all()           