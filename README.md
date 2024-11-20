# CarSphere web app
# Owner: Israel Wasserman (im.vaserman@gmail.com)
Description: Application for Cars review
Technical details:
   * languages: Python, HTML (jinja2), JavaScript
   * Framework: Flask
   * DB: SQLite using SQLAlchemy
      
Functional Information:
 * The application allows users to:
   - Sign-Up/Login.
   - Adding reviews for several Car models.
   - Generate an AI review, this feature connects to an external AI API service.
   - Admin functionality: admin users can also edit the Cars catalog by add/removing cars items using a dedicated User interface.

How to use:
 * Download the Repository
 * Go to project location
 * In terminal run the following commands:
    - 'python -m venv venv'
    - (Windows) 'venv\Scripts\activate'
    - (macOS/Linux) 'source venv/bin/activate'
    - 'pip install -r requirements.txt' 
    - Make sure all packages are successfully installed 'pip list' 
    - Run the app by running the following command 'python app.py'
    - go to the following URL in your browser 'http://127.0.0.1:5000'
    - Enjoy :)

Login credentials:
 * Admin user:
   - username: admin
   - password: admin

 * Non admin user:
   - username: user3
   - password: user3

* You may Signing-Up and using your own new user