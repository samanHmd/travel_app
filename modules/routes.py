from flask import Flask
from flask_restful import Api, Resource
from modules import app
from modules.controllers.homeController import HomeController
from modules.controllers.singinController import SignInController
from modules.controllers.loginController import LoginController
from modules.controllers.agentLoginController import AgentLoginController
from modules.controllers.agentSignupController import AgentSignupConroller
from modules.controllers.packageController import PackageController

api = Api(app)

api.add_resource(HomeController, '/')
api.add_resource(SignInController, '/register')
api.add_resource(LoginController, '/login')
api.add_resource(AgentLoginController, '/agentLogin')
api.add_resource(AgentSignupConroller, '/agentSignup')
api.add_resource(PackageController, '/packages')