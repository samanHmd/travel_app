from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with
from modules.Models import Agent
from modules import bcrypt, db, app
import jwt
from datetime import datetime, timedelta



class AgentSignupConroller(Resource):
    def get(self):
        return "agent signup get"

    def post(self):
        try:
            password = "123"
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            agent = Agent(name="agent", userName="agent", email="agent@mail.com", password=hashed)
            db.session.add(agent)
        except Exception as e:
            print(str(e)) 
            db.session.rollback()
            return {'error': str(e)}, 400
        finally:
            db.session.commit()
            agent = Agent.query.filter_by(userName="agent").first()
            encoded_jwt = jwt.encode({'user_id':agent.id, 'expiration': str(datetime.utcnow() + timedelta(seconds=172800))}, app.config['SECRET_KEY'], algorithm="HS256")
            return {"status": "success","api_token": encoded_jwt, "userName": agent.userName}, 200
            

        