from flask import render_template, redirect, url_for, flash
from bank import app
from bank.forms import RegForm, LogInForm


@app.route("/")
def home():
    return render_template("index.html", title="Home", logged_in=False)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    return render_template("login.html", title="Login", form=form, logged_in=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegForm()
    if form.validate_on_submit():
        flash('Thanks for registering, please login to continue!', 'success')
        return redirect(url_for("home"))
    if form.submit():
        print(form.errors)
    return render_template("register.html", title="Register", form=form)

@app.route("/tos")
def tos():
    return render_template("tos.html", title="Terms Of Service")


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 (page not found) errors by displaying 404 page with link to home page

    :param e: The error (in this case 404)
    :return: the 404 page
    """
    return render_template('404.html'), 404
