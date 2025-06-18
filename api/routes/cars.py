from flask_restx import Resource, Namespace, fields
from app.models import Car, db

cars_ns = Namespace('cars', description='Car operations')

# API model for swagger documentation
car_model = cars_ns.model('Car', {
    'make': fields.String(required=True, description='Car manufacturer'),
    'model': fields.String(required=True, description='Car model name'),
    'year': fields.Integer(required=True, description='Manufacturing year'),
    'description': fields.String(description='Car description'),
    'image_file': fields.String(description='Car image filename'),
    'director': fields.String(description='Car director'),
    'main_settings': fields.String(description='Car main settings')
})

@cars_ns.route('/')
class CarList(Resource):
    @cars_ns.doc('list_cars')
    def get(self):
        """List all cars"""
        cars = Car.query.all()
        return [{
            'id': car.id,
            'make': car.make,
            'model': car.model,
            'year': car.year,
            'description': car.description,
            'image_file': car.image_file,
            'director': car.director,
            'main_settings': car.main_settings
        } for car in cars]

    @cars_ns.doc('create_car')
    @cars_ns.expect(car_model)
    def post(self):
        """Create a new car"""
        data = cars_ns.payload
        car = Car(**data)
        db.session.add(car)
        db.session.commit()
        return {'message': 'Car created successfully'}, 201 