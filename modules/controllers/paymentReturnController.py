from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.Models import User, Package, PackageActivity, PackageFlight, PackageHotel
import jwt
from datetime import datetime, timedelta
from modules import db, app
import stripe



class PaymentReturnController(Resource):
    def get(self):
        
        return "create custom get"

    def post(self):
        
        print("Request data 0: ", request)  # raw request data
        print("Request data: ", request.data)  # raw request data
        print("Request headers: ", request.headers)  # request headers
        data = request.get_json()
        print("Parsed JSON data: ", data)
        return { "status": "success"}, 200
            