from app import app, mongo
from flask import jsonify
from flask import request, url_for, redirect
from werkzeug.http import HTTP_STATUS_CODES
from bson.objectid import ObjectId
from func_pack import create_rec_hash, str_to_right_type


# Get all competition infos
@app.route("/api/competition/all-competitions", methods=['GET'])
def get_all_competitions():
    data = list()
    for record in mongo.db.Competition.find():
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions info by its name
@app.route("/api/competition/competition-name/<string:competition_name>", methods=['GET'])
def get_competition_by_comp_name(competition_name):
    data = list()
    # maybe the competition_name in different items are same
    for record in mongo.db.Competition.find({"comp_title": competition_name}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its owner(contributor_id)
@app.route("/api/competition/contributor-id/<string:contributor_id>", methods=['GET'])
def get_competition_by_contributor_id(contributor_id):
    data = list()
    # maybe the contributor_id in different items are same
    for record in mongo.db.Competition.find({"contributor_id": contributor_id}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its hostname
@app.route("/api/competition/hostname/<string:hostname>", methods=['GET'])
def get_competition_by_comp_host_name(hostname):
    data = list()
    # maybe the hostname in different items are same
    for record in mongo.db.Competition.find({"comp_host_name": hostname}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its scenario
@app.route("/api/competition/scenario/<string:scenario>", methods=['GET'])
def get_competition_by_comp_scenario(scenario):
    data = list()
    # maybe the comp_scenario in different items are same
    for record in mongo.db.Competition.find({"comp_scenario": scenario}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its data feature
@app.route("/api/competition/data-feature/<string:data_feature>", methods=['GET'])
def get_competition_by_data_feature(data_feature):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Competition.find({"data_feature": data_feature}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get one competition info by its _id
@app.route("/api/competition/rid/<string:rid>", methods=['GET'])
def get_competition_by__id(rid):
    data = list()
    # Type 'ObjectId' in Pymongo come from bson.objectid.ObjectId
    oid = ObjectId(rid)
    # the _id is unique
    record = mongo.db.Competition.find_one_or_404({"_id": oid})
    record['_id'] = str(record['_id'])
    data.append(record)
    return jsonify(data)


# Insert new competition infos
@app.route("/api/competition", methods=['POST'])
def insert_new_competition():
    # Revert list-like string to list
    comp_scenario_list = str_to_right_type(request.form.get('comp_scenario'))
    comp_data_feature_list = str_to_right_type(request.form.get('data_feature'))

    # Revert dict-like string to dict
    comp_host_list = str_to_right_type(request.form.get('comp_host'))

    # assemble a dict
    new_competition = dict()
    new_competition['comp_record_hash'] = create_rec_hash()
    new_competition['comp_title'] = request.form.get('comp_title')
    new_competition['comp_subtitle'] = request.form.get('comp_subtitle')
    new_competition['comp_range'] = request.form.get('comp_range')
    new_competition['comp_url'] = request.form.get('comp_url')
    new_competition['comp_description'] = request.form.get('comp_description')
    new_competition['comp_host'] = comp_host_list
    new_competition['prize_amount'] = request.form.get('prize_amount')
    new_competition['prize_currency'] = request.form.get('prize_currency')
    new_competition['publish_time'] = request.form.get('publish_time')
    new_competition['update_time'] = request.form.get('update_time')
    new_competition['deadline'] = request.form.get('deadline')
    new_competition['timezone'] = request.form.get('timezone')
    # for multiple competition scenarios
    new_competition['comp_scenario'] = comp_scenario_list
    # for multiple competition data features
    new_competition['data_feature'] = comp_data_feature_list
    new_competition['contributor_id'] = request.form.get('contributor_id')

    oid = mongo.db.Competition.insert_one(new_competition).inserted_id
    rid = str(oid)

    # return redirect(url_for('get_competition_by__id', rid=rid))
    # return the success info
    return get_competition_by__id(rid=rid)


# Mention that all items are list type in this way
# # Insert new competition infos
# @app.route("/api/competition", methods=['POST'])
# def insert_new_competition():
#     # Here are the right way to write NoSQL receiver
#     new_competition = dict(request.form)
#
#     oid = mongo.db.Competition.insert_one(new_competition).inserted_id
#     rid = str(oid)
#
#     # return redirect(url_for('get_competition_by__id', rid=rid))
#     # return the success info
#     return get_competition_by__id(rid=rid)


# Modify an existed competition info
@app.route("/api/competition/<string:rid>", methods=['PUT'])
def update_competition(rid):
    # Revert list-like string to list
    comp_scenario_list = str_to_right_type(request.form.get('comp_scenario'))
    comp_data_feature_list = str_to_right_type(request.form.get('data_feature'))

    # Revert dict-like string to dict
    comp_host_list = str_to_right_type(request.form.get('comp_host'))

    # assemble a dict
    mod_competition = dict()
    mod_competition['comp_record_hash'] = request.form.get('comp_record_hash')
    mod_competition['comp_title'] = request.form.get('comp_title')
    mod_competition['comp_subtitle'] = request.form.get('comp_subtitle')
    mod_competition['comp_range'] = request.form.get('comp_range')
    mod_competition['comp_url'] = request.form.get('comp_url')
    mod_competition['comp_description'] = request.form.get('comp_description')
    mod_competition['comp_host'] = comp_host_list
    mod_competition['prize_amount'] = request.form.get('prize_amount')
    mod_competition['prize_currency'] = request.form.get('prize_currency')
    mod_competition['publish_time'] = request.form.get('publish_time')
    mod_competition['update_time'] = request.form.get('update_time')
    mod_competition['deadline'] = request.form.get('deadline')
    mod_competition['timezone'] = request.form.get('timezone')
    mod_competition['comp_scenario'] = comp_scenario_list
    mod_competition['data_feature'] = comp_data_feature_list
    mod_competition['contributor_id'] = request.form.get('contributor_id')

    # pymongo update dict structure
    set_dict = {"$set": mod_competition}

    oid = ObjectId(rid)
    mongo.db.Competition.update_one({"_id": oid}, set_dict)

    # return redirect(url_for('get_competition_by__id', rid=rid))
    # return the success info
    return get_competition_by__id(rid=rid)


# Delete an existed competition info
@app.route("/api/competition/<string:rid>", methods=['DELETE'])
def delete_competition(rid):
    set_dict = dict()
    oid = ObjectId(rid)
    set_dict['_id'] = oid
    mongo.db.Competition.delete_one(set_dict)
    data = [{'_id': rid, 'deleted status': 'success'}]
    return jsonify(data)


# Get competitions info by its name in fuzzy mode
@app.route("/api/competition/competition-name/fuzzy/<string:competition_name>", methods=['GET'])
def get_competition_by_comp_name_fuzzy(competition_name):
    data = list()
    # using fuzzy mode with regex
    for record in mongo.db.Competition.find({"comp_title": {'$regex': competition_name}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its hostname in fuzzy mode
@app.route("/api/competition/hostname/fuzzy/<string:hostname>", methods=['GET'])
def get_competition_by_comp_host_name_fuzzy(hostname):
    data = list()
    # maybe the hostname in different items are same
    for record in mongo.db.Competition.find({"comp_host.comp_host_name": {'$regex': hostname}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its scenario in fuzzy mode
@app.route("/api/competition/scenario/fuzzy/<string:scenario>", methods=['GET'])
def get_competition_by_comp_scenario_fuzzy(scenario):
    data = list()
    # maybe the comp_scenario in different items are same
    for record in mongo.db.Competition.find({"comp_scenario": {'$regex': scenario}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Get competitions by its data feature in fuzzy mode
@app.route("/api/competition/data-feature/fuzzy/<string:data_feature>", methods=['GET'])
def get_competition_by_data_feature_fuzzy(data_feature):
    data = list()
    # maybe the data_feature in different items are same
    for record in mongo.db.Competition.find({"data_feature": {'$regex': data_feature}}):
        record['_id'] = str(record['_id'])
        data.append(record)
    return jsonify(data)


# Fuzzy Search by comp_title, comp_host_name, comp_scenario or data_feature
@app.route("/api/competition/comp-search/fuzzy/<string:keyword>", methods=['GET'])
def search_competition_fuzzy_single_keyword(keyword):
    data = list()
    search_list = list()
    search_list.append({'comp_title': {'$regex': keyword}})
    search_list.append({'comp_host.comp_host_name': {'$regex': keyword}})
    search_list.append({'comp_scenario': {'$regex': keyword}})
    search_list.append({'data_feature': {'$regex': keyword}})

    # # 'and' search
    # for record in mongo.db.Competition.find({'$and': search_list}):
    #     record['_id'] = str(record['_id'])
    #     data.append(record)

    # 'or' search (using unique _id to make sure no duplication)
    for record in mongo.db.Competition.find({'$or': search_list}):
        record['_id'] = str(record['_id'])
        data.append(record)

    # Dedup no more
    # data_dedup = list(set(data))
    # data_dedup.sort(key=data.index)
    # return jsonify(data_dedup)
    return jsonify(data)


# Fuzzy Search in multiple by comp_title, comp_host_name, comp_scenario and data_feature
# @app.route("/api/competition/comp-search/fuzzy/multi/<string:keywords>", methods=['GET'])
# def search_competition_fuzzy_multi_keywords(keywords):
#     # keywords split by space
#     data = list()
#     search_dict = dict()
#     # split the string which include multiple keyword
#     key_words = keywords.split(' ').remove('')
#     print(key_words)


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
