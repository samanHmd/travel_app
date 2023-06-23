from flask import Flask, request, jsonify
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel
from modules.packageManagement.models.activity import Activity
from modules.packageManagement.models.package import Package
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta


class ReceiveDataController(Resource):
    def get(self):
        return "receive data get"

    def post(self):
        data = request.get_json()
        returnComponents_response = Package.returnComponents(data)
        return data
            