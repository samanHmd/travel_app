from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sshtunnel import SSHTunnelForwarder
import os



ssh_user = "ubuntu"
ssh_key_file = "C:\\Users\\a\\Desktop\\key\\privateKey.pem"
aws_host = "3.128.182.187"
remote_bind_address = "database-1.ccedoovh3jkf.us-east-2.rds.amazonaws.com"
db_user = "admin"
db_password = "Ss40000072!"
db_name = "travelDB"


app = Flask(__name__)
CORS(app)
api = Api(app)


if os.getenv('ENV') == 'production':
    print("DATABASE_URI: ", os.getenv('DATABASE_URI'))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
else:
    server = SSHTunnelForwarder(
        (os.getenv('SSH_HOST'), int(os.getenv('SSH_PORT'))),
        ssh_username=os.getenv('SSH_USERNAME'),
        ssh_private_key=os.getenv('SSH_KEY_FILE'),
        remote_bind_address=(os.getenv('DB_HOST'), int(os.getenv('DB_PORT')))
    )
    server.start()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://admin:Ss40000072!@127.0.0.1:{server.local_bind_port}/travelDB'
    import atexit
    atexit.register(server.stop)




app.config['SECRET_KEY'] = '94fjfj@/afd+kdioeur8349j3dljfa38]\kdu'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from modules import routes