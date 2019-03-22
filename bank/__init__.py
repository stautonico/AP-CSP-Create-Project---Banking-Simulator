from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize the instance of the web app
app = Flask(__name__)
# Define a secret key (for debugging and security)
app.config["SECRET_KEY"] = 'ad1d22ced33e1748caaaf681fd41b164d929abfef1b270f1b0123a3b7e3a7d39'
# Configure the url to the database (connection url)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
# create an instance of the database with the app as an argument (for connection and cooperation)
db = SQLAlchemy(app)

# create and instance of the bcrypt class with the app as an argument (for connection and cooperation)
bcrypt = Bcrypt(app)

# create and instance of the login_manager with the app as an argument (for connection and cooperation)
login_manager = LoginManager(app)
# Define the page where the login page exists (`def login()` in routes.py)
login_manager.login_view = 'login'
# Define the theme of the login messages (info is a bootstrap class that has a light blue color)
# (https://getbootstrap.com/docs/4.0/utilities/colors/)
login_manager.login_message_category = "info"

# Import routes after the app has been defined
# If this is at the top of the line, it would create a circular import loop
# This is due to the fact that the routes file needs to import from this file, and if it tries to import from this file
# with that line on the top, it will constantly try to cycle between importing itself and this file
from bank import routes
