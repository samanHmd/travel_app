from flask import Flask
from flask_restful import Api, Resource, request
from modules.userManagement.models.agent import Agent
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta


class AgentLoginController(Resource):
    def get(self):
        return "agent login get"

    def post(self):
        data = request.get_json()
        agentLogin_response = Agent.agentLogin(data)
        return agentLogin_response

        