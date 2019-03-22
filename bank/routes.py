from flask import render_template, redirect, url_for, flash, request
from bank import app, db, bcrypt
from bank.forms import RegForm, LogInForm, TransactionForm, AccountSearchForm, ReverseUserSearchForm, TransferMoneyForm
from bank.models import User, Transaction
from flask_login import login_user, logout_user, current_user, login_required
from random import randint


@app.route("/")
def home():
    """
    Homepage
    :return:
    """
    if current_user.is_authenticated:
        # If the user is logged in, grab any transaction they sent or received
        sent_transactions = Transaction.query.filter_by(sender=current_user.account_number).all()
        received_transactions = Transaction.query.filter_by(recipient=current_user.account_number).all()

        # if they have more then five transactions, grab the most recent 5 (to show recent transactions on home page)
        if len(sent_transactions) >= 5:
            sent_transactions = sent_transactions[:5]
        if len(received_transactions) >= 5:
            received_transactions = received_transactions[:5]

        return render_template("index.html", title="Home", sent_transactions=sent_transactions,
                               received_transactions=received_transactions)

    # if they aren't logged in, just display a regular home page (transaction display is handled by index.html)
    return render_template("index.html", title="Home")


@app.route("/login/", methods=["GET", "POST"])
def login():
    # Check if user is already logged in (redirect to home if they already are)
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Check if the user exists and if the password the user entered matches the hashed on in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            # Redirect them to the next page they were suppoed to go to, or just redirect them home if they weren't going anywhere
            # If the user tries to access the account without an account, there will be a next var,
            # then they will be redirected back to that account page after they successfully log in
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Please Check Email and Password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/register/", methods=["GET", "POST"])
def register():
    # Check if a user is already logged in (just redirect back home)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegForm()
    if form.validate_on_submit():
        # generate a hash for the password
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        free_account_number = False
        # ensure that no duplicate account numbers are generated (keep looping until one is generated that doesn't
        # already exist in the database)
        while not free_account_number:
            account_number = randint(10000000, 999999999999)
            if not User.query.filter_by(account_number=account_number).first():
                free_account_number = True
        # create an instance of a new user with the data the user entered (except use hashed password instead of plain
        # text version the user entered)
        new_user = User(username=form.username.data, email=form.email.data, password=password_hashed,
                        account_number=account_number, first_name=form.first_name.data, last_name=form.last_name.data)
        # add the user to the db and commit the changes
        db.session.add(new_user)
        db.session.commit()
        # Display success message and redirect to login page
        flash('Thanks for registering, please login to continue!', 'success')
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route('/logout/')
def logout():
    # Check if the user is logged in
    if current_user.is_authenticated:
        logout_user()
        flash("Logged out successfully!", "success")
        return redirect(url_for('home'))
    # if they aren't display a warning message and redirect to home page
    flash("No user is currently logged in", "warning")
    return redirect(url_for('home'))
    # The reason there is 2 separate `return redirect()` is so the warning message isn't displayed if the user is
    # logged in. If that return under the success message wasn't there, the success and the warning message would
    # both be displayed and then redirected.


@app.route("/transaction/", methods=["GET", "POST"])
@login_required
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        recipient_user = User.query.filter_by(account_number=form.recipient.data).first()

        transaction = Transaction(sender=current_user.account_number, recipient=recipient_user.account_number,
                                  amount=float(form.amount.data))
        # remove the amount from the senders checking and add it to the recipients checking acount
        current_user.checking -= float(form.amount.data)
        recipient_user.checking += float(form.amount.data)
        # Add the newly created transaction record to the database and commit the change in user amounts
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
        # If the user selected savings (transfer money FROM checking TO savings)
        if form.account.data == "Savings":
            # Check if the user has enough money in their checking
            if current_user.checking < float(form.amount.data):
                flash("You do not have enough money to transfer!", "danger")
                return redirect(url_for('transfer'))
            # If they do have enough money
            else:
                # Subtract from checking and add to savings
                current_user.checking -= float(form.amount.data)
                current_user.savings += float(form.amount.data)
                db.session.commit()
                flash(f"Successfully transferred ${form.amount.data} to {form.account.data}", "success")
            return redirect(url_for('account'))
        # If the user selected checking (transfer money FROM savings TO checking)
        else:
            # Check if the user has enough in their savings
            if current_user.savings < float(form.amount.data):
                flash("You do not have enough money to transfer!", "danger")
                return redirect(url_for('transfer'))
            # If the user has enough
            else:
                # Subtract from savings and add to checking
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
    # Get all of the transactions that was sent by the user or received by the user
    sent_transactions = Transaction.query.filter_by(sender=current_user.account_number).all()
    received_transactions = Transaction.query.filter_by(recipient=current_user.account_number).all()
    # Pass the received and sent transactions to the html file ("account.html" iterates and displays the data)
    return render_template("account.html",
                           title=f"{current_user.username}", sent_transactions=sent_transactions,
                           received_transactions=received_transactions)


@app.route("/account/search/", methods=["GET", "POST"])
@login_required
def account_search():
    form = AccountSearchForm()
    if form.validate_on_submit():
        # Check if there is a user record that has this data (ALL OF IT)
        user = User.query.filter_by(first_name=form.first_name.data, last_name=form.last_name.data,
                                    email=form.email.data).first()
        # If the user record exists in the db
        if user:
            # Display the account number in a flash message
            flash(f"Found user: {user.account_number}", "success")
        else:
            # Otherwise, display an error message (flashed)
            flash("No user found.", "warning")
    return render_template("account_search.html", title="Find An Account", form=form)


@app.route("/account/search-reverse/", methods=["GET", "POST"])
@login_required
def account_search_reverse():
    form = ReverseUserSearchForm()
    if form.validate_on_submit():
        # Query database to see if there is a user that has that account number
        user = User.query.filter_by(account_number=form.account_number.data).first()
        # If there is a user record, flash the first and last name
        if user:
            flash(f"Found user: {user.first_name} {user.last_name}", "success")
        # Otherwise, flash an error message
        else:
            flash("No user found.", "warning")
    return render_template("reverse_account_search.html", title="Reverse Account Search", form=form)


# Handles 404 errors (if the user goes to a url/page that doesn't exist, display `404.html` instead
@app.errorhandler(404)
def page_not_found(e):
    """
    Handle 404 (page not found) errors by displaying 404 page with link to home page

    :param e: The error (in this case 404)
    :return: the 404 page
    """
    return render_template('404.html'), 404
