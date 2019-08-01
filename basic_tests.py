from app import mongo

if __name__ == '__main__':

    c = {
        "competition_name": "abcdefg"
    }

    record_id = mongo.db.Competition.insert_one(c).insert_id

    pass


