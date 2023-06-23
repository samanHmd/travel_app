from flask import Flask, request, jsonify,redirect
from flask_restful import Api, Resource, fields, marshal_with, marshal
from modules.packageManagement.models.package import Package, PackageActivity, PackageFlight, PackageHotel
from modules.userManagement.models.user import User
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timedelta
from modules import db, app
import stripe

stripe.api_key = 'sk_test_Hrs6SAopgFPF0bZXSN3f6ELN'
YOUR_DOMAIN = 'http://3.128.182.187/static-page'


class CreatePackageController(Resource):
    def get(self):
        return "create custom get"

    def post(self):
        data = request.get_json()
        createCustomPackage_response = Package.createCusotmPackage(data)
        return createCustomPackage_response

        
            