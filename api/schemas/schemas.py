from marshmallow import Schema, fields

class CarSchema(Schema):
    """Schema for Car model serialization/deserialization"""
    id = fields.Int(dump_only=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    year = fields.Int(required=True)
    description = fields.Str()
    image_file = fields.Str()
    director = fields.Str()
    main_settings = fields.Str()

class ReviewSchema(Schema):
    """Schema for Review model serialization/deserialization"""
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    user_id = fields.Int(required=True)
    car_id = fields.Int(required=True) 