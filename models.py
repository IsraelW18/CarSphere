import time
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import random
import forms

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(150), unique=False, nullable=False, default='')
    last_name = db.Column(db.String(150), unique=False, nullable=False, default='')
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.jpg')
    registration_datetime = db.Column(db.String(150), unique=False, nullable=True, default=datetime.now())
    admin = db.Column(db.Boolean, default=False)

    def set_username(self, _username):
        self.username = _username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def set_profile_image(self):
    #     random_image = random.choice(['profile1.jpg', 'profile2.jpg', 'profile3.jpg'])
    #     self.profile_image = random_image

    def set_current_time(self):
        self.registration_datetime = datetime.now()

    def set_firstname(self, _firstname):
        self.first_name = _firstname

    def set_lastname(self, _lastname):
        self.last_name = _lastname

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    director = db.Column(db.String(100), nullable=True)
    main_settings = db.Column(db.String(200), nullable=True)
    reviews = db.relationship('Review', backref='car', lazy=True)

    def __repr__(self):
        return f"Car('{self.make}', '{self.model}', '{self.year}', '{self.image_file}')"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    # Define the relationship to the User model
    user = db.relationship('User', backref='reviews', lazy=True)