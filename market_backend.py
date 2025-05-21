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
    

    def generate_testing_data(self):
        for x in range(100):
            self.db.add_prod(f"Produto {x}", 10000, 100)

    # Vender produto
    def sell(self, prod_id, quantity):
        product = self.db.get_prod(prod_id)

        if not product:
            raise exceptions.ProdNotFoundException("Produto não encontrado")
        else:
            if product['stock'] < quantity:
                raise exceptions.NotEnoughItemsException("Quantidade insuficiente")
            else:
                # Colocar a venda
                ''' Como colocar na lista:
                    {
                        "prod": product,
                        "prod_id": product['id'],
                        "quantity": quantity,
                        "total_sold": product['price'] * quantity,
                        "total_profit": product['profit'] * quantity
                    }
                '''


                self.current_transaction.append({
                    "prod": product,
                    "prod_id": product['id'],
                    "quantity": quantity,
                    "total_sold": product['price'] * quantity,
                    "total_profit": product['profit'] * quantity
                })


    def finish_transaction(self):
        # Primeiro, atualizar o estoque
        for transaction in self.current_transaction:
            self.db.prod_stock_update(transaction['prod_id'], transaction["prod"]["stock"] - transaction["quantity"])


if __name__ == "__main__":
    market = Market("config.json")
    market.generate_testing_data()
    market.sell(2, 10)
    print(market.current_transaction)
    market.finish_transaction()

