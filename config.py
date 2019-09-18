import os
basedir = os.path.abspath(os.path.dirname(__file__))
import time


class Config(object):

    MONGO_HOST = os.environ.get('DSC_COMPETITION_MONGODB_SERVICE_HOST')
    MONGO_PORT = os.environ.get('DSC_COMPETITION_MONGODB_SERVICE_PORT')

    MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
    MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_PROTOCOL = os.environ.get('MONGO_PROTOCOL')

    SECRET_KEY = os.environ.get('WEB_SERVER_SECRET_KEY') or 'abcdef020301abc8c86f'

    # MONGO_URI = "mongodb://dbuser:dbpassword@174.137.53.253:27017/testdb"
    MONGO_URI = MONGO_PROTOCOL + '://' + MONGO_USERNAME + ':' + MONGO_PASSWORD + '@' + \
                MONGO_HOST + ':' + MONGO_PORT + '/' + MONGO_DBNAME
