from pymongo import MongoClient

from config.server import environment

mongo_config = environment.mongo

client = MongoClient(host=mongo_config.host, port=mongo_config.port)

db = client[mongo_config.db]
