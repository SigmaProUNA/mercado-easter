import json
import market_backend
import finances
import front_utils
import fastmath
import exceptions
import sys

from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTableView, QComboBox, QDialog, QGridLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel


# Editor do banco
class DbEditor(QDialog):
    def __init__(self, config: dict, backend: market_backend.Market):
        super().__init__()
        self.setWindowTitle("Easter")

        self.main_layout = QVBoxLayout()
        self.backend = backend
        self.config = config
        self.lang_dict = self.config["words"][self.config["selected_lang"]]

        # COmeçar a fazer a UI

        # Escolher ação
        self.top_layout = QHBoxLayout()
        self.action_combobox = QComboBox()
        self.actions_choose = [self.lang_dict["add"], self.lang_dict["remove"], self.lang_dict["edit"]]

        self.action_combobox.addItems(self.actions_choose)

        # Botão de fazer a ação
        self.action_button = QPushButton(self.lang_dict["do_action"])
        self.action_button.clicked.connect(self.on_action)

        self.top_layout.addWidget(self.action_combobox)
        self.top_layout.addWidget(self.action_button)
        # Inputs:
        self.input_layout = QGridLayout()

        self.prod_id = [QLabel(self.lang_dict["id"]), QLineEdit()]
        self.name = [QLabel(self.lang_dict["name"]), QLineEdit()]
        self.base_price = [QLabel(self.lang_dict["base_price"]), QLineEdit()]
        self.stock = [QLabel(self.lang_dict["quantity"]), QLineEdit()]

        row = 0
        for i in [self.prod_id, self.name, self.base_price, self.stock]:
            column = 0
            for val in i:
                self.input_layout.addWidget(val, row, column)
                column += 1

            row += 1

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.input_layout)
        self.setLayout(self.main_layout)


    def on_action(self):
        action = self.action_combobox.currentIndex()

        # Primeiro checar se tem id do produto e se é valido
        prod_id = self.prod_id[1].text()
        if fastmath.is_integer(prod_id) and prod_id != "":
            prod_id = int(prod_id)
        else:
            if action != 0:
                front_utils.message(2, f"{self.lang_dict['invalid_id']}")
                return
        
        inputs = [self.name[1].text(), self.base_price[1].text(), self.stock[1].text()]

        # Procurar por inputs que deveriam ser inteiros
        integer_indexes = [1, 2]
        for i in inputs:
            input_index = inputs.index(i) 
            input_text = i
            if input_text != "":
                if not fastmath.is_integer(input_text) and input_index in integer_indexes:
                    front_utils.message(2, f"{self.lang_dict['invalid_input_int']}")
                    return
                else:
                    inputs[input_index] = finances.money_to_cents(input_text)

        if action == 0:
            # Todos os campos precisam ter valores nesse caso
            for i in inputs:
                if i == "":
                    front_utils.message(2, f"{self.lang_dict['empty_fields_noid']}")
                    return

            self.backend.add_prod(inputs[0], inputs[1], inputs[2])
        elif action == 1:
            try:
                self.backend.remove_prod(prod_id)
            except exceptions.ProdNotFoundException:
                front_utils.message(2, f"{self.lang_dict['prod_not_found']}")
                return
        elif action == 2:
            try:
                self.backend.update_prod(prod_id, inputs[0], inputs[1], inputs[2])
            except exceptions.ProdNotFoundException:
                front_utils.message(2, f"{self.lang_dict['prod_not_found']}")

        front_utils.message(0, f"{self.lang_dict['action_done']}")
        self.close()
        return
            

# Front end
class MarketWindow(QMainWindow):
    def __init__(self, config: str):
        super().__init__()
        self.setWindowTitle("Easter")
        self.setMinimumSize(531, 400)
        
        # Configurações
        self.config = json.loads(open(config, "r").read())
        self.lang_dict = self.config["words"][self.config["selected_lang"]]
        front_utils.LANG_DICT = self.lang_dict # Definir a lingua do bagulho
        

        # Classe do backend
        self.backend = market_backend.Market(config)

        # Widget central
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Layouts para a UI
        self.layouts = {
            "top_bar": [QHBoxLayout()],
            "pay_price": [QVBoxLayout()],
            "transaction": [QHBoxLayout()],
            "bottom_bar": [QHBoxLayout()]
        }
        
        # Adicionar no central e já ir colocando widgets
        for key, val in self.layouts.items():
            add_stetch = False #  Para adicionar stretch
            stetch_index = 0 # O indice
            
            self.main_layout.addLayout(val[0])
            
            # Lista de widgets
            widgets = []
            
            if key == "top_bar":
                widgets = [[QLabel("Easter")],
                [QComboBox(), [self.lang_dict["daily"], self.lang_dict["weekly"], self.lang_dict["all_time"]]],
                [QPushButton(f"{self.lang_dict['gen_report']}"), self.on_generate],
                [QPushButton(f"{self.lang_dict['db_edit']}"), self.on_db_edit]]
                
                # Negrito no label 0
                widgets[0][0].setStyleSheet("font-weight: bold; font-size: 30px")
                add_stetch = True
                stetch_index = 1
            elif key == "pay_price":
                widgets = [[
                    QLabel(f"{self.lang_dict['total_sold']}:")],
                    [QLabel(finances.cents_to_money(0, self.config["money_unit"], self.config["decimal_place"], self.config["separator"]))]
                ]
                
                for w in widgets:
                    # Editar o widget para deixar negrito
                    w[0].setStyleSheet("font-weight: bold; font-size: 20px")
                    w[0].setAlignment(Qt.AlignmentFlag.AlignCenter)
            elif key == "transaction":
                widgets = [[QTableView(), [self.lang_dict["id"], self.lang_dict["item_id"], self.lang_dict["product"], self.lang_dict["quantity"], self.lang_dict["price"]], QStandardItemModel()]]

                # Adicionar header da tabela
                for w in widgets:
                    if isinstance(w[0], QTableView):
                        w[2].setColumnCount(len(w[1]))
                        w[2].setRowCount(1)
                        w[2].setHorizontalHeaderLabels(w[1])
                        w[0].setModel(w[2])
                            
            
            elif key == "bottom_bar":
                widgets = [[QPushButton(f"{self.lang_dict['search']}"), self.on_search],
                           [QPushButton(f"{self.lang_dict['add_prod']}"), self.on_add_prod],
                           [QPushButton(f"{self.lang_dict['rem_prod']}"), self.on_rem_prod],
                           [QPushButton(f"{self.lang_dict['finish']}"), self.on_finish_transac]]
            
            index = 0
            for w in widgets:
                if stetch_index == index and add_stetch:
                    val[0].addStretch(1)
                
                val[0].addWidget(w[0])

                if len(w) > 1:
                    if isinstance(w[0], QPushButton):
                        w[0].clicked.connect(w[1]) # type: ignore
                    elif isinstance(w[0], QComboBox):
                        w[0].addItems(w[1]) # type: ignore
                
                index += 1
                   
            val.append(widgets)
            
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        
        self.__init_vars__()

    
    # Variáveis
    def __init_vars__(self):
        self.cents_total = 0
        self.price_label = self.layouts["pay_price"][1][1][0]
        self.table = self.layouts["transaction"][1][0]
        self.table_model = self.table[2]
        self.item_id_index = 1
        self.cents_per_row = [] # Armazenar o valor original de centavos para linha
        self.report_combobox = self.layouts["top_bar"][1][1][0]

    # Adicionar produto na transação
    def on_add_prod(self):
        prod_id = front_utils.ask_input(self.lang_dict["ask_id_desc"], self.lang_dict["ask_id_title"], input_type=int)
        quanitity = front_utils.ask_input(self.lang_dict["ask_quantity_desc"], self.lang_dict["ask_quantity_title"], input_type=int)        
        
        # Checa se o input não é vazio, se não for, continua
        if prod_id != "" and quanitity != "":
            try:
                transaction = self.backend.sell(int(prod_id), int(quanitity))
            except exceptions.ProdNotFoundException:
                front_utils.message(2, f"{self.lang_dict['prod_not_found']}")
                return
            except exceptions.NotEnoughItemsException:
                front_utils.message(2, f"{self.lang_dict['not_enough_items']}")
                return
            
            # Adicionar a tabela
            
            model = self.table_model
            row_num = model.rowCount()
            column_num = model.columnCount()
            
            # Conseguir a proxima linha
            row = 0
            for row in range(row_num):
                if model.data(model.index(row, 0)) is None or model.data(model.index(row, 0)) == "":
                    break
            
            if row == row_num-1:
                model.insertRow(row_num)
                
            # Adicionar na linha a transação
            data = [transaction["prod_id"], transaction["item_id"], transaction["name"], transaction["quantity"], finances.cents_to_money(transaction["total_sold"], self.config["money_unit"], self.config["decimal_place"], self.config["separator"])]
            for col in range(column_num):
                model.setData(model.index(row, col), data[col])
                
            
            # Adicionar ao valor
            cents = int(transaction["total_sold"])
            self.cents_per_row.append(cents)
            self.cents_total += cents
            self.price_label.setText(finances.cents_to_money(self.cents_total, self.config["money_unit"], self.config["decimal_place"], self.config["separator"]))


    # Remover da transação e da tabela
    def on_rem_prod(self):
        item_id = front_utils.ask_input(self.lang_dict["ask_item_id_desc"], self.lang_dict["ask_item_id_title"], input_type=int)
        
        # Procurar o ID da transação na tabela, e se achar remover
        for row in range(self.table_model.rowCount()):
            item_id_r = self.table_model.data(self.table_model.index(row, self.item_id_index))
            
            if item_id_r is None or item_id_r == "":
                break # FIm da lista com valores
            
            price = self.cents_per_row[row]
            if int(item_id_r) == int(item_id):
                self.backend.cancel_item(int(item_id))
                self.table_model.removeRow(row)
                self.cents_total -= price
                self.price_label.setText(finances.cents_to_money(self.cents_total, self.config["money_unit"], self.config["decimal_place"], self.config["separator"]))
                self.cents_per_row.pop(row)
                return
        
        # Se chegou nessa parte, provavelmente não foi encontrado
        front_utils.message(2, f"{self.lang_dict['item_not_found']}")
    
    
    # Finaliza transação
    def on_finish_transac(self):
        try:
            self.backend.finish_transaction()
            self.cents_per_row = []
            self.cents_total = 0
            self.price_label.setText(finances.cents_to_money(self.cents_total, self.config["money_unit"], self.config["decimal_place"], self.config["separator"]))
            
            # limpar a tabela
            for row in range(self.table_model.rowCount()):
                for column in range (self.table_model.columnCount()):
                    self.table_model.setData(self.table_model.index(row, column), "")
            
            front_utils.message(0, f"{self.lang_dict['transac_finished']}")
        except exceptions.NotEnoughItemsException:
            front_utils.message(2, f"{self.lang_dict['not_enough_items']}")
            return
    
    
    def on_search(self):
        search = front_utils.ask_input(self.lang_dict["ask_search_desc"], self.lang_dict["ask_search_title"])
        result = self.backend.search(search)
        
        headers = [self.lang_dict["id"], self.lang_dict["product"], self.lang_dict["price"], self.lang_dict["quantity"]]
        row_indexes = [0, 1, 4, 5]
        money_indexes = [4]
        
        rows = []
        for row in result["rows"]:
            filtered_row = []
            for indx in row_indexes:
                item = row[indx]
                
                # Se o index for monetário, transformar
                if indx in money_indexes:
                    item = finances.cents_to_money(int(item), self.config["money_unit"], self.config["decimal_place"], self.config["separator"])
                
                filtered_row.append(item)
                
            rows.append(filtered_row)   
        
        front_utils.table_dialog(self.lang_dict["search_res_title"], self.lang_dict["search_res_desc"], headers, rows)


    # Gerar o relatório com base na escolha
    def on_generate(self):
        choice = self.report_combobox.currentIndex()
        
        report = open(self.backend.generate_report(choice), "r").read()
        
        front_utils.show_markdown(report, self.lang_dict["report_title"])
        

    def on_db_edit(self):
        editor = DbEditor(self.config, self.backend)
        editor.exec()

