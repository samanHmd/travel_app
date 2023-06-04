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
        data = request.get_json()
        print("dataaaaaaaaa",data)
        return { "status": "success"}, 200
            