from flask import Flask, jsonify
from flask_restful import Api, Resource, request, fields, marshal_with, marshal
from modules.Models import User, Package
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta





class BookingController(Resource):
    def get(self):
        
        return 'booking get'

    def post(self):
        return 'booking post'