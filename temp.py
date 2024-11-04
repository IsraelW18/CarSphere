from app import app, db
from models import User  # Make sure to import your User model

# Create a function to update the admin status
def update_admin_status(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            user.admin = 1  # Change admin status to 1
            db.session.commit()  # Commit the changes to the database
            print(f"User {user_id} admin status updated to {user.admin}.")
        else:
            print(f"User with id {user_id} not found.")

# Call the function with the user ID you want to update
update_admin_status(1)  # Replace 1 with the actual user ID