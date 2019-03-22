from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from bank.models import User
from flask_login import current_user

class RegForm(FlaskForm):
    """
    The form template for account registration
    """
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password')])
    terms_of_service = BooleanField("I agree to The Terms of Service", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """
        Validate if the username is already taken

        :param username: The entered username
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken.")

    def validate_email(self, email):
        """
        Validate if an email is already in use

        :param email: The entered email
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already taken.")


class LogInForm(FlaskForm):
    """
    The form for logging in to an existing account
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class TransactionForm(FlaskForm):
    """
    The form for sending money to different users
    """
    recipient = StringField("Recipient", validators=[DataRequired(), Length(min=8, max=12)])
    amount = StringField("Amount", validators=[DataRequired()])
    submit = SubmitField("Send")

    def validate_recipient(self, recipient):
        """
        Validate if the user exists or if the recipient user is the current user

        :param recipient: The account number entered into the form
        :return:
        """
        if current_user.account_number == int(recipient.data):
            raise ValidationError("You cannot send money to yourself.")
        recipient = User.query.filter_by(account_number=recipient.data).first()
        if not recipient:
            raise ValidationError("No user with that account number exists.")

    def validate_amount(self, amount):
        """
        Validate if the current user has enough money in his/her account to send (checking)

        :param amount: The amount that the user is trying to send
        :return:
        """
        if current_user.checking < float(amount.data):
            raise ValidationError("You do not have enough money to send.")
        if float(amount.data) <= 0:
            raise ValidationError("You must send at least one dollar.")


class TransferMoneyForm(FlaskForm):
    """
    The form for transferring money between accounts (checking and savings)
    """
    account = RadioField("Account To Transfer To", choices=[('Checking', 'Checking'), ('Savings', 'Savings')],
                         validators=[DataRequired()])
    amount = StringField("How Much To Transfer", validators=[DataRequired()])
    submit = SubmitField("Transfer")


class AccountSearchForm(FlaskForm):
    """
    The form for finding account numbers from first name, last name, and email
    """
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Find")


class ReverseUserSearchForm(FlaskForm):
    """
    The form for finding who owns an account from the account number
    """
    account_number = StringField("Account Number", validators=[DataRequired(), Length(min=8, max=12)])
    submit = SubmitField("Find")
