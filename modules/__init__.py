from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
api = Api(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://samHmd:S40000072@samHmd.mysql.pythonanywhere-services.com/traveldb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '94fjfj@/afd+kdioeur8349j3dljfa38]\kdu'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from modules import routes