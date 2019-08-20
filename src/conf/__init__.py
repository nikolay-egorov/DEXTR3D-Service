import os, configparser, sys
from pymongo import MongoClient


def initConfig():
    dir_path = os.path.dirname(os.path.abspath(__file__))

    config = configparser.ConfigParser()
    dir_path = dir_path + '/conf.ini'

    # dataset= config.read('{dir_path}\\conf.ini')

    # if len(dataset) != len(1):
    #     raise ValueError("Failed to open/find all files")
    try:
        with open(dir_path) as f:
            config.read_file(f)
    except IOError:
        raise ValueError("Failed to open/find all files")

    return config


def initMongoDBConn(component=None):
    config = initConfig()

    try:
        client = MongoClient('{host}:{port}'.format(host=config['mongodb']['host'], port=config['mongodb']['port']))
        mongodb_conn = client[config[component]['collection']]
    except ValueError as e:
        print('MongoDB connection to {host} is refused'.format(host=config['mongodb']['host']))
        sys.exit()

    return mongodb_conn