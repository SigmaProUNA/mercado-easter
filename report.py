import os
import datetime

# Classe para reportar vendas no arquivo de vendas em CSV
class SellReport:
    def __init__(self, path: str):
        self.path = path
        self.delimiter = ";"
        self.header = ["id", "date", "prod_id", "quantity", "total_sold", "total_profit"]
        self.id_index = 0 # O index responsável pelo id
        self.datetime_format = "%Y-%m-%d"
    

    # Consegue o proximo id de venda
    def _next_id(self):
        csv = open(f"{self.path}", "r").readlines()
        highest = 0
        
        if len(csv) > 1:
            for line in csv:
                line = line.replace("\n", "") # Tira \n no final
                columns = line.split(self.delimiter)

                sell_id = int(columns[self.id_index])
                if sell_id > highest:
                    highest = sell_id

        return highest + 1

    
    # Inicializa o arquivo csv
    def initialize(self):
        if not os.path.exists(self.path):
            # Inicializa o CSV com o header
            f = open(f"{self.path}", "w+")
            
            f.write(self.delimiter.join(self.header)+"\n")

            f.close()
    
    # Reporta no arquivo CSV de venda
    def report(self, prod_id: int, quantity: int, total_sold: int, total_profit: int):
        # Consegue o id e a data formatada para o csv
        sell_id = self._next_id()
        date = datetime.datetime.now().strftime(self.datetime_format)

        # Linha
        row = [sell_id, date, prod_id, quantity, total_sold, total_profit]
        row = [str(r) for r in row] # Converte cada item para str

        # Adicionar no arquivo csv
        csv_f = open(self.path, "a")
        csv_f.write(self.delimiter.join(row)+"\n")
        csv_f.close()


if __name__ == "__main__":
    report = SellReport("sell.csv")
    report.initialize()
    report.report(1, 1, 1, 1)
