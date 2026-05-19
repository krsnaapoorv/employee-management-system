from flask import Blueprint

routes = Blueprint('routes', __name__)

# Import controllers to register routes
from .employee_controller import *
