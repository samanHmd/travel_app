from flask import Flask, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import Flight, Hotel, Activity
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta


class ReceiveDataController(Resource):
    def get(self):
        return "receive data get"

    def post(self):
        data = request.get_json()
        check_in_date = datetime.strptime(data["check_in_date"], '%Y-%m-%d')
        check_out_date = datetime.strptime(data["check_out_date"], '%Y-%m-%d')
        flights = Flight.query.filter_by(departureCity= data.get('departureCity'), arrivalCity=data.get('destinationCity')).all()
        flights = Flight.query.filter_by(arrivalCity=data.get('destinationCity')).all()
        print(flights)
        return {"status": "success","flights": [flight.as_dict() for flight in flights]}, 200
            