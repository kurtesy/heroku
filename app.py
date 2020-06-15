from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import dev
from api_auth import require_appkey
from utils import generateId, prepareData, error_response
from database.customer import Customer, BillPayment

app = Flask(dev.APP_NAME)

app.config.from_pyfile('./config/dev.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/api/v1/', methods=['GET'])
def index():
    return jsonify({'title': 'Welcome to Setu API endpoint',
                    'app_name': dev.APP_NAME})


@app.route('/api/v1/fetch-bill', methods=['POST'])
@require_appkey
def fetch_bill():
    try:
        if not request.json or not 'mobileNumber' in request.json:
            error_response("invalid-api-parameters", 402)
        mobile_number = request.json['mobileNumber']
        row = Customer.query.filter_by(mobile_number=mobile_number).first()
        if row:
            return jsonify({
                    "status": "SUCCESS",
                    "data": row.serialize()
                }), 201
        else:
            error_response("customer-not-found", 406)
    except Exception as err:
        error_response("unhandled-error", 408)


@app.route('/api/v1/payment-update', methods=['POST'])
@require_appkey
def payment_update():
    postData = request.json
    rowInsert = prepareData(postData)
    print 'INSERT IT', rowInsert
    #Check if ref_id already exist
    row = BillPayment.query.filter_by(ref_id=rowInsert['ref_id']).first()
    if row:
        return jsonify({
            "status": "SUCCESS",
            "data": {
                "ackID": row.ack_id
            }
        }), 202
    else:
        key = generateId()
        transactionRow = BillPayment(date=rowInsert['date'],
                                     amount_paid=rowInsert['amount_paid'],
                                     id=rowInsert['id'],
                                     ref_id=rowInsert['ref_id'],
                                     ack_id=key)
        db.session.add(transactionRow)
        db.session.commit()
        return jsonify({
                "status": "SUCCESS",
                "data": {
                    "ackID": key
                }
            }), 201


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def fallback(u_path):
    error_response("path-not-found", 404)


if __name__ == '__main__':
    db.create_all()
    db.session.commit()
    app.run(debug=True)
