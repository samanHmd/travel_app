from flask import Flask, jsonify
from flask_restful import Resource, request
from faker import Faker
import random
from datetime import datetime, timedelta
from modules.userManagement.models.user import User
from modules.packageManagement.models.package import Package, PackageHotel, PackageFlight, PackageActivity
from modules.packageManagement.models.flight import Flight
from modules.packageManagement.models.hotel import Hotel 
from modules.packageManagement.models.activity import Activity
from modules import db
from modules.data import flights_data, hotels_data, activities_data, packages_data




class PackageController(Resource):
    def get(self):
        getPackages_response = Package.getPackages()
        return getPackages_response
        
        
    def post(self):
        createPreDefineSamples_response = Package.createPreDefineSamples(self)
        return createPreDefineSamples_response
    
    def delete(self):
        data = request.get_json()
        preDefineDelete_response = Package.preDefineDelete(data)
        return preDefineDelete_response