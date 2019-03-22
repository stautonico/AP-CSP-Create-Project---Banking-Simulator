from bank import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    Grab user (used for login) (flask_login uses this to manage logged in users)

    :param user_id: The user's id in the database
    :return:
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    The database model for user accounts

    id: auto-assigned, database assigns an id to each user
    username: The users username
    email: the users email
    first_name: The users first name
    last_name: The users surname
    account_number: auto-assigned, account number given to all users (send and receive money)
    checking: balance in the user's checking account
    savings: balance in the user's savings account
    """
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
        """
        What is returned when a user instance is printed

        :return:
        """
        return f"User('{self.id}', {self.username}, {self.account_number})"


class Transaction(db.Model):
    """
    The database model for a transaction between users

    id: auto-assigned, id for each transaction (internal)
    sender: the sender of the money (initiator of transaction)
    recipient: the user who receives the transaction (money)
    amount: the amount sent through the transaction
    date: a timestamp when the transaction was sent
    """
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer(), nullable=False)
    recipient = db.Column(db.Integer(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)
    date = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __repr__(self):
        """
        What is returned when a transaction instance is printed
        :return:
        """
        return f"Transaction('{self.sender}', {self.recipient}, {self.amount}, {self.date})"
