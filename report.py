import os
import finances
import database
import datetime
import json

# Classe para reportar vendas no arquivo de vendas em CSV
class SellReport:
    def __init__(self, path: str, config: str, db: database.Database):
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
        self.db = db
    

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
    def generate_day_report(self, today_only: bool = True, time_range: int = 7, since_epoch: bool = False):
        
        # SObreescrever o range se since_epoch
        if since_epoch:
            time_range = round(datetime.datetime.now().timestamp() / 86400) # para dias
        
        md_text = "" # O report será feito em markdown
        today = datetime.datetime.now().strftime(self.datetime_format) if today_only else None # Só do dia aatual caso today
        csv = [x.strip().replace("\n", "") for x in open(self.path, "r").readlines()] # CSV


        # TAbela de vendas
        md_text += f"# {self.lang_dict['sellings']}\n"
        md_text += f"| {self.lang_dict['data']}    | {self.lang_dict['value']} |\n"
        
        total_quantity = 0
        total_sold = 0
        total_profit = 0

        line_index = 0  
        
        dates = []
        
        filename = ""
        # Lista de datas para pegar
        if today_only:
            dates = [today]
            filename = today
        else:
            for x in range(time_range):
                dates.append((datetime.datetime.now() - datetime.timedelta(days=x)).strftime(self.datetime_format))
            
            filename = f"{dates[-1]}_to_{dates[0]}"
            
        print(dates)
              
        # Pegar os dados
        for today in dates:
            for line in csv:
                line = line.split(self.delimiter)
                
                if line_index > 0 and line[self.date_index] == today and len(line) > 1:
                    total_quantity += int(line[self.quantity_index])
                    total_sold += int(line[self.total_sold_index])
                    total_profit += int(line[self.total_profit_index])

                line_index += 1


        # Adicionar na tabela
        md_text += f"| {self.lang_dict['quantity_sold']} | {total_quantity} |\n"
        md_text += f"| {self.lang_dict['total_sold']} | {finances.cents_to_money(total_sold)} |\n"
        md_text += f"| {self.lang_dict['daily_profit']} | {finances.cents_to_money(total_profit)} |\n"
        
        # Sessão de ranking de produtos mais vendidos do dia
        md_text += f"\n# {self.lang_dict['best_sellers']}\n"
        
        # Ranqueamento
        prod_list = []
        for today in dates:
            for line in csv:
                line = line.split(self.delimiter)
                if line[self.date_index] == today:
                    prod_id = int(line[self.prod_id_index])
                    prod_info = db.get_prod(prod_id)
                    prod_list.append([prod_info['name'], prod_id, line[self.quantity_index]])

        # Juntar produtos com mesmo id 
        prod_list_copy = [x for x in prod_list]
        already_found = []
        for item in prod_list:
            is_unique = True # Se é unico
            
            # Se a lista ta vazia, tem nada então nem tem por que iterae
            if len(already_found) <= 0:
                already_found.append(item)
                continue
            
            for found in already_found:
                if found[1] == item[1]:
                    found[2] = int(found[2]) + int(item[2])
                    prod_list_copy.remove(item)
                    is_unique = False
                    break
            
            if is_unique:
                already_found.append(item)
                
            print(already_found)
            print(prod_list_copy)
            print(flush=True)

            
        prod_list = [x for x in already_found]
        prod_list.sort(key=lambda x: int(x[2]), reverse=True)
        
        # Adicionar no arquivo
        md_text += f"| {self.lang_dict['product']} | {self.lang_dict['quantity_sold']} |\n"
        
        for prod in prod_list:
            print(prod, flush=True)
            md_text += f"| {prod[0]} | {prod[2]} |\n"
                
        # Salva o markdown
        os.makedirs(self.config['report_path'], exist_ok=True)
        open(f"{self.config['report_path']}/{filename}.md", "w+").write(md_text)

    # Função wrapper para evitar confusões... poderia ser feito manualmente.
    def generate_week_report(self):
        self.generate_day_report(False, 7)
        
    
    # Função wrapper para todos os tempos...
    def generate_all_time_report(self):
        self.generate_day_report(False, since_epoch=True)


if __name__ == "__main__":
    db = database.Database("database.db")
    db.initialize()
    db.set_profit(10)
    db.add_prod("Teste", 100, 100)
    report = SellReport("sell.csv", "config.json", db)
    report.initialize()
    report.report(1, 1, 1, 3)
    report.generate_day_report()
    report.generate_week_report()
    report.generate_all_time_report()
