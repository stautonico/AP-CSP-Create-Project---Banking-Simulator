from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from bank.models import User
from flask_login import current_user


class RegForm(FlaskForm):
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
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already taken.")


class LogInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class TransactionForm(FlaskForm):
    recipient = StringField("Recipient", validators=[DataRequired(), Length(min=8, max=12)])
    amount = StringField("Amount", validators=[DataRequired()])
    submit = SubmitField("Send")

    def validate_recipient(self, recipient):
        if current_user.account_number == int(recipient.data):
            raise ValidationError("You cannot send money to yourself.")
        recipient = User.query.filter_by(account_number=recipient.data).first()
        if not recipient:
            raise ValidationError("No user with that account number exists.")

    def validate_amount(self, amount):
        if current_user.checking < float(amount.data):
            raise ValidationError("You do not have enough money to send.")
        if float(amount.data) <= 0:
            raise ValidationError("You must send at least one dollar.")


class TransferMoneyForm(FlaskForm):
    account = RadioField("Account To Transfer To", choices=[('Checking', 'Checking'), ('Savings', 'Savings')],
                         validators=[DataRequired()])
    amount = StringField("How Much To Transfer", validators=[DataRequired()])
    submit = SubmitField("Transfer")


class AccountSearchForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Find")


class ReverseUserSearchForm(FlaskForm):
    account_number = StringField("Account Number", validators=[DataRequired(), Length(min=8, max=12)])
    submit = SubmitField("Find")
