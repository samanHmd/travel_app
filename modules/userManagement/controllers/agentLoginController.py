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

        required_fields = ['userName', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return {"error": f"{field} is required."}, 400
            

        agent = Agent.query.filter_by(userName=data.get('userName')).first()
        if agent:
            if bcrypt.check_password_hash(agent.password, data.get('password')):
                encoded_jwt = jwt.encode({'user_id':agent.id, 'expiration': str(datetime.utcnow() + timedelta(seconds=172800))}, app.config['SECRET_KEY'], algorithm="HS256")
                return {"status": "success","api_token": encoded_jwt, "userName": agent.userName}, 200
            else: return { "status": "Password doesn't match" }
        else:
            return { "status": "No Such Agent" }