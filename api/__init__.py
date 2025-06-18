from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp,
          title='Cars API',
          version='1.0',
          description='RESTful API for Cars Web Application',
          doc='/docs')

# Import and register namespaces
from .routes.cars import cars_ns
from .routes.reviews import reviews_ns

api.add_namespace(cars_ns)
api.add_namespace(reviews_ns) 