from flask import render_template
from bank import app


@app.route("/")
def home():
    return render_template("index.html", title="Home")


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/register")
def register():
    return render_template("register.html", title="Register")


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 (page not found) errors by displaying 404 page with link to home page

    :param e: The error (in this case 404)
    :return: the 404 page
    """
    return render_template('404.html'), 404
