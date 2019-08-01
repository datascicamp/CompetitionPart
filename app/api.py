from app import app, mongo
from flask import jsonify
from flask import request, url_for, redirect
from flask_pymongo import PyMongo
from werkzeug.http import HTTP_STATUS_CODES
from bson.objectid import ObjectId


# Get all competition infos
@app.route("/api/all-competitions")
def get_all_competitions():
    data = list()
    for record in mongo.db.Competition.find():
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get one competition info by its name
@app.route("/api/competition/competition_name/<string:competition_name>")
def get_competition_by_competition_name(competition_name):
    data = list()
    # maybe the competition_name in different items are same
    for record in mongo.db.Competition.find({"competition_name": competition_name}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get one competition info by its _id
@app.route("/api/competition/rid/<string:rid>")
def get_competition_by_id(rid):
    data = list()
    # Type 'ObjectId' in Pymongo come from bson.objectid.ObjectId
    oid = ObjectId(rid)
    # the _id is unique
    record = mongo.db.Competition.find_one_or_404({"_id": oid})
    record['_id'] = str(record['_id'])
    data.append(record)
    return jsonify(data)

# # get account by account_id
# @app.route('/api/account-id/<int:account_id>', methods=['GET'])
# def get_user_by_uid(account_id):
#     data = list()
#     data.append(Account.query.get_or_404(account_id).to_dict())
#     return jsonify(data)
#
#
# # get account by account_email
# @app.route('/api/account-email/<string:account_email>', methods=['GET'])
# def get_user_by_username(account_email):
#     data = list()
#     data.append(Account.query.filter(Account.account_email == account_email).first_or_404().to_dict())
#     return jsonify(data)
#
#
# # get account by account_status
# @app.route('/api/account-status/<string:account_status>', methods=['GET'])
# def get_user_by_phone_number(account_status):
#     data = list()
#     for account in Account.query.filter(Account.account_status == account_status).all():
#         data.append(account.to_dict())
#     return jsonify(data)
#
#
# # get all accounts
# @app.route('/api/all-accounts', methods=['GET'])
# def get_all_users():
#     data = list()
#     for account in Account.query.all():
#         data.append(account.to_dict())
#     return jsonify(data)
#
#
# # create new account
# @app.route('/api/create-account', methods=['POST'])
# def create_new_user():
#     account_email = request.form.get('account_email')
#     password = request.form.get('password')
#     email = request.form.get('email')
#     phone_number = request.form.get('phone_number')
#
#     # check faults
#     if password is None or username is None:
#         return bad_request('This post must include both username and password fields.')
#     if email is None or phone_number is None:
#         return bad_request('This post must include both email and phone_number fields.')
#     if User.query.filter_by(username=username).first():
#         return bad_request('please use a different username.')
#     if User.query.filter_by(email=email).first():
#         return bad_request('please use a different email address.')
#     if User.query.filter_by(phone_number=phone_number).first():
#         return bad_request('please use a different phone number.')
#
#     # db operations
#     new_user = User(username=username, email=email, phone_number=phone_number)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()
#
#     # response data
#     data = list()
#     # This username is the one which user input in POST form
#     data.append(User.query.filter(User.username == username).first_or_404().to_dict())
#
#     return jsonify(data)
#
#
# # update user info
# @app.route('/users', methods=['PUT'])
# def update_user():
#     username = request.form.get('username')
#     if username is None:
#         return bad_request('This post must include username field.')
#
#     # get PUT data
#     password = request.form.get('password') or None
#     email = request.form.get('email') or None
#     phone_number = request.form.get('phone_number') or None
#
#     # take out data form db
#     user = User.query.filter_by(username=username).first()
#
#     # update procedure
#     if password is not None:
#         user.set_password(password)
#     if email is not None:
#         user.email = email
#     if phone_number is not None:
#         user.phone_number = phone_number
#
#     # update db
#     db.session.add(user)
#     db.session.commit()
#
#     # response data
#     data = list()
#     # This username is the one which user input in POST form
#     data.append(User.query.filter(User.username == username).first_or_404().to_dict())
#
#     return jsonify(data)
#
#
# # verify username and password
# @app.route('/users/validation/', methods=['POST'])
# def validate_password():
#     # Get user information from POST
#     username = request.form.get('username')
#     password = request.form.get('password')
#
#     # if there is no password field in post
#     if password is None or username is None:
#         return bad_request('This post must include both username and password fields.')
#     user = User.query.filter(User.username == username).first()
#     if user is None:
#         return jsonify([{'uid': -1, 'username': username, 'validation': 'False'}])
#     validate = user.check_password(password)
#
#     # authentication verify success.
#     if validate is True:
#         return jsonify([{'uid': user.id, 'username': username, 'validation': 'True'}])
#     # authentication verify failed.
#     return jsonify([{'uid': -1, 'username': username, 'validation': 'False'}])


# bad requests holder
def bad_request(message):
    return error_response(400, message)


# error response
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response
