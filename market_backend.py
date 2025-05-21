import database
import finances
import csv
import exceptions
import json


class Market():
    def __init__(self, config_path):
        self.config = json.load(open(config_path))
        self.db = database.Database(self.config['db_path'])
        self.db.initialize()
        self.db.set_profit(self.config['profit'])

        self.current_transaction = []


    # Vender produto
    def sell(self, prod_id, quantity):
        product = self.db.get_prod(prod_id)

        if not product:
            raise exceptions.ProdNotFoundException("Produto não encontrado")
        else:
            pass

