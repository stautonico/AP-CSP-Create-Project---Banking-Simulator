from flask import render_template, redirect, url_for, flash, request
from bank import app, db, bcrypt
from bank.forms import RegForm, LogInForm, TransactionForm, AccountSearchForm, ReverseUserSearchForm, TransferMoneyForm
from bank.models import User, Transaction
from flask_login import login_user, logout_user, current_user, login_required
from random import randint


@app.route("/")
def home():
    if current_user.is_authenticated:
        sent_transactions = Transaction.query.filter_by(sender=current_user.account_number).all()
        received_transactions = Transaction.query.filter_by(recipient=current_user.account_number).all()

        if len(sent_transactions) >= 5:
            sent_transactions = sent_transactions[:5]
        if len(received_transactions) >= 5:
            received_transactions = received_transactions[:5]

        return render_template("index.html", title="Home", sent_transactions=sent_transactions,
                               received_transactions=received_transactions)

    return render_template("index.html", title="Home")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please Check Email and Password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        free_account_number = False
        while not free_account_number:
            account_number = randint(10000000, 999999999999)
            if not User.query.filter_by(account_number=account_number).first():
                free_account_number = True
        new_user = User(username=form.username.data, email=form.email.data, password=password_hashed,
                        account_number=account_number, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering, please login to continue!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route('/logout/')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out successfully!", "success")
        return redirect(url_for('home'))
    flash("No user is currently logged in", "warning")
    return redirect(url_for('home'))


@app.route("/transaction/", methods=["GET", "POST"])
@login_required
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        recipient_user = User.query.filter_by(account_number=form.recipient.data).first()

        transaction = Transaction(sender=current_user.account_number, recipient=recipient_user.account_number,
                                  amount=float(form.amount.data))

        current_user.checking -= float(form.amount.data)
        recipient_user.checking += float(form.amount.data)
        db.session.add(transaction)
        db.session.commit()
        flash(f"Successfully sent ${form.amount.data} to {form.recipient.data}!", "success")
        return redirect(url_for("home"))
    return render_template("transaction.html", form=form, title="Send Money")


@app.route("/transfer/", methods=["GET", "POST"])
@login_required
def transfer():
    form = TransferMoneyForm()
    if form.validate_on_submit():
        if form.account.data == "Savings":
            if current_user.checking < float(form.amount.data):
                flash("You do not have enough money to transfer!", "danger")
                return redirect(url_for('transfer'))
            else:
                current_user.checking -= float(form.amount.data)
                current_user.savings += float(form.amount.data)
                db.session.commit()
                flash(f"Successfully transferred ${form.amount.data} to {form.account.data}", "success")
            return redirect(url_for('account'))
        else:
            if current_user.savings < float(form.amount.data):
                flash("You do not have enough money to transfer!", "danger")
                return redirect(url_for('transfer'))

            else:
                current_user.checking += float(form.amount.data)
                current_user.savings -= float(form.amount.data)
                db.session.commit()
                flash(f"Successfully transferred ${form.amount.data} to {form.account.data}", "success")
            return redirect(url_for('account'))

    return render_template("transfer.html", title="Transfer Money", form=form)


@app.route("/tos/")
def tos():
    return render_template("tos.html", title="Terms Of Service")


@app.route("/account/")
@login_required
def account():
    sent_transactions = Transaction.query.filter_by(sender=current_user.account_number).all()
    received_transactions = Transaction.query.filter_by(recipient=current_user.account_number).all()

    return render_template("account.html",
                           title=f"{current_user.username}", sent_transactions=sent_transactions,
                           received_transactions=received_transactions)


@app.route("/account/search/", methods=["GET", "POST"])
@login_required
def account_search():
    form = AccountSearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data,
                                    email=form.email.data).first()
        if user:
            flash(f"Found user: {user.account_number}", "success")
        else:
            flash("No user found.", "warning")
    return render_template("account_search.html", title="Find An Account", form=form)


@app.route("/account/search-reverse/", methods=["GET", "POST"])
@login_required
def account_search_reverse():
    form = ReverseUserSearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account_number=form.account_number.data).first()
        if user:
            flash(f"Found user: {user.first_name} {user.last_name}", "success")
        else:
            flash("No user found.", "warning")
    return render_template("reverse_account_search.html", title="Reverse Account Search", form=form)


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 (page not found) errors by displaying 404 page with link to home page

    :param e: The error (in this case 404)
    :return: the 404 page
    """
    return render_template('404.html'), 404
