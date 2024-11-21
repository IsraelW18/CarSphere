import sqlite3
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, AddCarForm, ReviewForm
from models import User, Car, Review
from models import db
import os
from werkzeug.utils import secure_filename
import requests
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.urandom(24)  # יצירת מפתח

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.set_username(form.username.data)
        user.set_password(form.password.data)
        user.set_firstname(form.firstname.data)
        user.set_lastname(form.lastname.data)
        # user.set_profile_image()  # Set a random profile image
        user.set_current_time()
        db.session.add(user)
        db.session.commit()

        login_user(user)

        flash(f"Welcome, {user.first_name} {user.last_name} and thanks for registration!<br><br>"
              f"!!! You're already logged-in. Let's Begin !!! ", 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)  # Logs the user in
            flash(f'Welcome, {user.first_name} {user.last_name}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Add a route for car details
@app.route('/car/<int:car_id>', methods=['GET', 'POST'])
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    form = ReviewForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            review = Review(content=form.review.data, car_id=car.id, user_id=current_user.id)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been added!', 'success')
            return redirect(url_for('car_detail', car_id=car.id))
    reviews = Review.query.filter_by(car_id=car_id).all()
    return render_template('car_detail.html', car=car, form=form, reviews=reviews)

# Add a route for handling review submissions
@app.route('/add_review/<int:car_id>', methods=['POST'])
@login_required
def add_review(car_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(content=form.review.data, car_id=car_id, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully!', 'success')
    return redirect(url_for('car_detail', car_id=car_id))

########################
# AI Review Generation:
@app.route('/generate_ai_review/<string:make>/<string:model>')
def generate_ai_review(make, model):
    # Define the API endpoint and request payload
    api_url = "https://api-inference.huggingface.co/models/gpt2"  # Free-tier Hugging Face API
    headers = {"Authorization": f"Bearer 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"}
    # Sending the request to the AI service in order to get a review based on the car "make" parameter in DB
    prompt = f"Write me a short review for a Car {make} {model}."

    # Make a POST request to generate text
    response = requests.post(api_url, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        raw_review = response.json()[0]['generated_text']
        # Logging
        print(f"Raw review returned from AI service:\n {raw_review}\n")
        # Cleaning the 'prompt' value from the 'review' returned from the AI service
        review = raw_review.replace(prompt, "")
        # Logging
        print(f"Clean review after removing the prompt:\n {review}")
    else:
        review = "Sorry, could not generate a review at this time."

    # Return JSON response
    return jsonify({"review": review})

@app.route('/all_rights', methods=['GET'])
def all_rights():
    cars = Car.query.all()
    return render_template('all_rights.html')

########################
## App & DB Maintenance
# Deleting all users from user table in DB
@app.route('/get-users')
def get_users():
    # עדכן את השם אם הוא שונה
    db_path = os.path.join(app.instance_path, 'site.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM user")  # החלף users בשם הטבלה שלך
    rows = cursor.fetchall()
    connection.close()

    return [''.join(row) for row in rows]

@app.route('/delete_all_users', methods=['GET'])
def delete_all_users():
    try:
        db.session.query(User).delete()
        db.session.commit()
        flash("All users have been deleted.", 'success')
    except Exception as e:
        db.session.rollback()  # In case of error rolling back the changes
        flash(f"An error occurred when trying delete all users: {e}", 'danger')
    return redirect(url_for('home'))

# Deleting all cars from car table in DB
@app.route('/delete_all_cars', methods=['GET'])
def delete_all_cars():
    try:
        db.session.query(Car).delete()
        db.session.commit()
        flash("All cars have been deleted.", 'success')
    except Exception as e:
        db.session.rollback()  # In case of error rolling back the changes
        flash(f"An error occurred when trying delete all cars: {e}", 'danger')
    return redirect(url_for('home'))

# Deleting all reviews from review table in DB
@app.route('/delete_all_reviews', methods=['GET'])
def delete_all_reviews():
    try:
        db.session.query(Review).delete()
        db.session.commit()
        flash("All reviews have been deleted.", 'success')
    except Exception as e:
        db.session.rollback()  # In case of error rolling back the changes
        flash(f"An error occurred when trying delete all reviews: {e}", 'danger')
    return redirect(url_for('home'))

# Creating Routes for Adding and Removing Cars
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    form = AddCarForm()
    # Generating the year dropdown list entries in add_car.html
    current_year = datetime.now().year
    years_list = reversed(range(1980, current_year + 1))
    years = [*years_list]
    form.year.choices = years

    if form.validate_on_submit() and request.method == 'POST':  # Check if form is valid and if it's a POST request
        # Process the form data
        make = form.make.data
        model = form.model.data
        year = form.year.data
        director = form.director.data
        main_settings = form.main_settings.data
        description = form.description.data
        # Check if a file was uploaded and if it's allowed
        image_file = request.files['image_file']
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)  # Save the uploaded image
        else:
            filename = 'default.jpg'  # Use a default image if no valid file was uploaded

        # Create and add the new car record
        car = Car(make=make, model=model, year=year, director=director, main_settings=main_settings, description=description, image_file=filename)
        db.session.add(car)
        db.session.commit()

        flash(f'Car {make} {model} added successfully!', 'success')
        return redirect(url_for('home'))

    # Render the form for 'GET' request to show the add_car page
    return render_template('add_car.html', form=form)


# Route for deleting a car
@app.route('/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    # Checking if the current user is authenticated or not admin
    if not current_user.is_authenticated or not current_user.admin:
        flash('Access Denied! Only admins can delete cars', 'danger')
        return redirect(url_for('home'))
    # If the user is authenticated and admin, deleting the relevant car according the car_id got as a
    # parameter in the route.
    # Deleting a Car for DB will be allowed only if the Car do not include User Reviews,
    # so before deleting - we will check if the Car includes any user review by the following 2 steps.
    #
    # Step_1: Collecting all 'car_id' exist in the Review table.
    review_details = Review.query.all()
    car_id_in_review_table = []
    for car_id_rev in review_details:
        car_id_in_review_table.append(car_id_rev.car_id)
    # Step_2: Checking if the current 'car_id' exist in the Review table.
    if car_id in car_id_in_review_table:
        # If so, delete process will not be allowed and relevant message will be displayed to the user.
        flash('Car includes user reviews and cannot be deleted !', 'danger')
        return redirect(url_for('home'))
    # If the current 'car_id' do not included in the Review table, it means that it do not include
    # user reviews and can be deleted.
    else:
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        flash('Car deleted successfully!', 'success')
        return redirect(url_for('home'))

################################

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)