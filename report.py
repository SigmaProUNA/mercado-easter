import os
import finances
import datetime
import json

# Classe para reportar vendas no arquivo de vendas em CSV
class SellReport:
    def __init__(self, path: str, config: str):
        self.path = path
        self.delimiter = ";"
        self.header = ["id", "date", "prod_id", "quantity", "total_sold", "total_profit"]
        self.id_index = 0 # O index responsável pelo id
        self.date_index = 1
        self.prod_id_index = 2
        self.quantity_index = 3
        self.total_sold_index = 4
        self.total_profit_index = 5
        self.datetime_format = "%Y-%m-%d"
        self.config = json.load(open(config, "r"))
        self.lang_dict = self.config["words"][self.config["selected_lang"]] # Lingua selecionada
    

    # Consegue o proximo id de venda
    def _next_id(self):
        csv = open(f"{self.path}", "r").readlines()
        highest = 0
        
        if len(csv) > 1:
            for line in csv:
                line = line.replace("\n", "") # Tira \n no final
                columns = line.split(self.delimiter)

                raw_id = columns[self.id_index]
                sell_id = int(raw_id) if raw_id.isnumeric() else 0
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

    
    # Gerar o report de lucro e produtos mais vendidos no dia
    def generate_day_report(self):
        md_text = "" # O report será feito em markdown
        today = datetime.datetime.now().strftime(self.datetime_format)
        csv = [x.strip().replace("\n", "") for x in open(self.path, "r").readlines()] # CSV


        # TAbela de vendas
        md_text += f"# {self.lang_dict['sellings']}\n"
        md_text += f"| {self.lang_dict['data']}    | {self.lang_dict['value']} |\n"
        
        total_quantity = 0
        total_sold = 0
        total_profit = 0

        line_index = 0

        # Pegar os dados
        for line in csv:
            line = line.split(self.delimiter)
            
            if line_index > 0 and line[self.date_index] == today:
                total_quantity += int(line[self.quantity_index])
                total_sold += int(line[self.total_sold_index])
                total_profit += int(line[self.total_profit_index])

            line_index += 1


        # Adicionar na tabela
        md_text += f"| {self.lang_dict['quantity_sold']} | {total_quantity} |\n"
        md_text += f"| {self.lang_dict['total_sold']} | {finances.cents_to_money(total_sold)} |\n"
        md_text += f"| {self.lang_dict['daily_profit']} | {finances.cents_to_money(total_profit)} |\n"

        # Salva o markdown
        os.makedirs(self.config['report_path'], exist_ok=True)
        open(f"{self.config['report_path']}/{today}.md", "w+").write(md_text)



if __name__ == "__main__":
    report = SellReport("sell.csv", "config.json")
    report.initialize()
    report.report(1, 1, 1, 3)
    report.generate_day_report()
