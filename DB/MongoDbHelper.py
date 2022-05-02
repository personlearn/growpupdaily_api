from ast import Import
import pymongo
import configHelper


class MongoDbHelper(object):
    def __init__(self, dbname):
        self.cl = pymongo.MongoClient(configHelper.getConfig(
            "mongodb", "host"), int(configHelper.getConfig("mongodb", "port")))
        self.db = self.cl[dbname]

    def getDb(self, table):
        return self.db[table]
