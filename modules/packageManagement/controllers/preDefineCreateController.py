from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.userManagement.models.user import User
from modules.packageManagement.models.package import Package, PackageActivity, PackageFlight, PackageHotel
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel
from modules.packageManagement.models.activity import Activity
from modules import bcrypt, app, db
import jwt
from datetime import datetime, timedelta





class PreDefineCreateController(Resource):
    def get(self):
        data = request.get_json()
        decoded_jwt = jwt.decode(data.get('api_token'), app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_jwt

    def post(self):
        data = request.get_json()
        preDefineCreate_response = Package.createPreDefine(data)
        return preDefineCreate_response
        
        

    def put(self):
        data = request.get_json()
        preDefineUpdate = Package.preDefineUpdate(data)
        return preDefineUpdate    
    
    