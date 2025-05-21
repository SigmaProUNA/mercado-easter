import database
import finances
import csv
import json


class Market():
    def __init__(self, config_path):
        self.config = json.load(open(config_path))
        self.db = database.Database(self.config['db_path'])
        self.db.initialize()
        self.db.set_profit(self.config['profit'])
        

