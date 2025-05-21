import csv
import os

# Classe para reportar vendas no arquivo de vendas em CSV
class SellReport:
    def __init__(self, path: str):
        self.path = path
        self.delimiter = ";"
        self.header = ["id", "date", "prod_id", "quantity", "total_sold", "total_profit"]

    
    # Inicializa o arquivo csv
    def initialize(self):
        if not os.path.exists(self.path):
            # Inicializa o CSV com o header
            f = open(f"{self.path}", "w+")
            
            f.write(self.delimiter.join(self.header))

            f.close()


if __name__ == "__main__":
    report = SellReport("sell.csv")
    report.initialize()
