import string
import random
from inflection import underscore
from flask import jsonify, abort, make_response

from database.customer import Customer, BillPayment


def error_response(errorCode, httpStatus):
    abort(
        make_response(
            jsonify({
                "status": "ERROR",
                "errorCode": errorCode
            }), httpStatus))


def generateId():
    rows = BillPayment.query.all()
    ids = []
    for row in rows:
        ids.append(row.ref_id)
    key = ''
    maxSearch = 50
    cnt=0
    while key not in ids and cnt < maxSearch:
        key = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(8)])
        cnt += 1
    return key


def prepareData(postData):
    print postData['transaction']
    fields = ['refID', 'date', 'id', 'amountPaid']
    if not postData or not 'refID' in postData and not 'transaction' in postData:
        error_response("invalid-api-parameters", 402)
    rowInsert = {}
    for field in fields:
        if field in postData:
            rowInsert[underscore(field)] = postData[field]
        elif field in postData['transaction']:
            rowInsert[underscore(field)] = postData['transaction'][field]
        else:
            error_response("invalid-api-parameters", 402)
    validateData(rowInsert['ref_id'], rowInsert['amount_paid'])
    return rowInsert


def validateData(ref_id, amount_paid):
    customerRow = Customer.query.filter_by(ref_id=ref_id).first()
    if customerRow:
        if float(customerRow.due_amount) != float(amount_paid):
            error_response('amount-mismatch', 403)
    else:
        error_response('invalid-ref-id', 405)