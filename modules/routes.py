from flask import Flask
from flask_restful import Api, Resource
from modules import app


from modules.userManagement.controllers.singinController import SignInController
from modules.userManagement.controllers.loginController import LoginController
from modules.userManagement.controllers.agentLoginController import AgentLoginController
from modules.userManagement.controllers.agentSignupController import AgentSignupConroller
from modules.userManagement.controllers.reportController import ReportController

from modules.packageManagement.controllers.packageController import PackageController
from modules.packageManagement.controllers.receiveDataController import ReceiveDataController
from modules.packageManagement.controllers.createPackageController import CreatePackageController
from modules.packageManagement.controllers.preDefineCreateController import PreDefineCreateController

from modules.bookingManagement.controllers.paymentReturnController import PaymentReturnController
from modules.bookingManagement.controllers.bookingController import BookingController
from modules.bookingManagement.controllers.viewBookingController import ViewBookingController
from modules.bookingManagement.controllers.viewPaymentController import ViewPaymentController


api = Api(app)

#userManagement Routes
api.add_resource(SignInController, '/register')
api.add_resource(LoginController, '/login')
api.add_resource(AgentLoginController, '/agentLogin')
api.add_resource(AgentSignupConroller, '/agentSignup')
api.add_resource(ReportController, '/report')

#packageManagement Routes
api.add_resource(PackageController, '/packages')
api.add_resource(ReceiveDataController, '/receiveData')
api.add_resource(CreatePackageController, '/createPackage')
api.add_resource(PreDefineCreateController, '/preDefineCreate')

#bookingManagement Routes
api.add_resource(PaymentReturnController, '/receiveStatusPayment')
api.add_resource(BookingController, '/booking')
api.add_resource(ViewBookingController, '/viewBooking')
api.add_resource(ViewPaymentController, '/viewPayment')
