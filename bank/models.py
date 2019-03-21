from bank import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(), unique=False, nullable=False)
    last_name = db.Column(db.String(), unique=False, nullable=False)
    account_number = db.Column(db.Integer(), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    checking = db.Column(db.Float(), default=0.00)
    savings = db.Column(db.Float(), default=0.00)

    def __repr__(self):
        return f"User('{self.id}', {self.username}, {self.account_number})"


class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer(), nullable=False)
    recipient = db.Column(db.Integer(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __repr__(self):
        return f"Transaction('{self.sender}', {self.recipient}, {self.amount}, {self.date})"
