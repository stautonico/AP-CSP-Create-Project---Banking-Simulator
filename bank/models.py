from bank import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    account_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    checking = db.Column(db.Integer, default=0)
    savings = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User('{self.id}', {self.username}, {self.account_number})"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender = db.Column(db.Integer, nullable=False)
    recipient = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Transaction('{self.sender}', {self.recipient}, {self.amount}, {self.date})"
