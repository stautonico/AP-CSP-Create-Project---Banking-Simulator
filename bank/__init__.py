from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = 'ad1d22ced33e1748caaaf681fd41b164d929abfef1b270f1b0123a3b7e3a7d39'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
db = SQLAlchemy(app)

from bank import routes
