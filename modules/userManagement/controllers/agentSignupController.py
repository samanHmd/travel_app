from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with
from modules.userManagement.models.agent import Agent
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta



class AgentSignupConroller(Resource):
    def get(self):
        return "agent signup get"

    def post(self):
        agentRegister_response = Agent.agentRegister()
        return agentRegister_response
            

        