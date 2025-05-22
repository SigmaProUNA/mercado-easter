import database
import report
import exceptions
import json


class REPORT_TYPES:
    DAY = 1
    WEEK = 2
    ALL_TIME = 3


class Market():
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = json.load(open(config_path))
        self.db = database.Database(self.config['db_path'])
        self.db.initialize()
        self.db.set_profit(self.config['profit'])

        self.csv = report.SellReport(self.config['sell_csv_path'], self.config_path, self.db)
        self.csv.initialize()
        
        self.current_transaction = []
    

    def generate_testing_data(self):
        for x in range(100):
            self.db.add_prod(f"Produto {x}", 10000, 10000000)

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
            stock = transaction["prod"]["stock"] - transaction["quantity"]
            if stock < 0:
                raise exceptions.NotEnoughItemsException(f"Quantidade insuficiente no estoque de {transaction['prod']['name']}")
            
            self.db.prod_stock_update(transaction['prod_id'], stock)
        
        # Adiciona a venda no CSV
        for transaction in self.current_transaction:
            self.csv.report(transaction['prod_id'], transaction['quantity'], transaction['total_sold'], transaction['total_profit'])

        # Finalizar a transação
        self.current_transaction = []
        
    
    # Gerar o relatório
    def generate_report(self, tp: int):
        file = ""
        
        if tp == REPORT_TYPES.DAY:
            file = self.csv.generate_day_report()
        elif tp == REPORT_TYPES.WEEK:
            file = self.csv.generate_week_report()
        elif tp == REPORT_TYPES.ALL_TIME:
            file = self.csv.generate_all_time_report()
        else:
            raise Exception(f"Invalid report type. Use a variable from REPORT_TYPES class.")
        
        return file
        

if __name__ == "__main__":
    pass
