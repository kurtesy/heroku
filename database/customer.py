from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import dev

app = Flask(dev.APP_NAME)
db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    mobile_number = db.Column(db.String(20))
    customer_name = db.Column(db.String(255))
    due_amount = db.Column(db.Float(2))
    due_date = db.Column(db.Text)
    ref_id = db.Column(db.String(20))

    def __init__(self, mobile_number):
        self.mobile_number = mobile_number

    def serialize(self):
        return {
                    "customerName": self.customer_name,
                    "dueAmount": self.due_amount,
                    "dueDate": self.due_date,
                    "refID": self.ref_id
                }


class BillPayment(db.Model):
    __tablename__ = 'bill_payment'
    id = db.Column(db.Integer)
    ref_id = db.Column(db.String(20), primary_key=True)
    amount_paid = db.Column(db.Float(2))
    date = db.Column(db.Text)
    ack_id = db.Column(db.String(20))

    def __init__(self, **kwargs):
        super(BillPayment, self).__init__(**kwargs)

    def serialize(self):
        return {
                    "refID": self.ref_id,
                    "amountPaid": str(self.amount_paid),
                    "date": self.date,
                    "id": self.id
                }


if __name__ == '__main__':
    db.create_all()
