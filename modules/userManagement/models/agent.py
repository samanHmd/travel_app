from modules import db, app
from datetime import datetime
from sqlalchemy.orm import class_mapper
from sqlalchemy import event
from modules import bcrypt, app
import jwt
from datetime import datetime, timedelta



class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    userName = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def agentLogin(data):
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


    def agentRegister():
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


with app.app_context():
    db.create_all()    