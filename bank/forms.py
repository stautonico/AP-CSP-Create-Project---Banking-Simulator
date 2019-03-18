from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo


class RegForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo('password'), Length(min=4)])
    terms_of_service = BooleanField("I agree to The Terms of Service", validators=[DataRequired()])
    submit = SubmitField("Register")


class LogInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")
