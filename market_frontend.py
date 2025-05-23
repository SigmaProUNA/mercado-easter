import json
import market_backend
import finances
import front_utils
import fastmath
import exceptions

from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTableView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem


# Front end
class MarketWindow(QMainWindow):
    def __init__(self, config: str):
        super().__init__()
        self.setWindowTitle("Easter")
        self.setMinimumSize(600, 400)
        
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
            self.main_layout.addLayout(val[0])
            
            # Lista de widgets
            widgets = []
            
            if key == "top_bar":
                widgets = [[QLabel("Easter")],
                [QPushButton(f"{self.lang_dict['gen_report']}")],
                [QPushButton(f"{self.lang_dict['db_edit']}")]]
                
                # Negrito no label 0
                widgets[0][0].setStyleSheet("font-weight: bold;")
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
                widgets = [[QTableView(), [self.lang_dict["id"], self.lang_dict["product"], self.lang_dict["quantity"], self.lang_dict["price"]], QStandardItemModel()]]

                # Adicionar header da tabela
                for w in widgets:
                    if isinstance(w[0], QTableView):
                        w[2].setColumnCount(len(w[1]))
                        w[2].setRowCount(100)
                        w[2].setHorizontalHeaderLabels(w[1])
                        w[0].setModel(w[2])
                            
            
            elif key == "bottom_bar":
                widgets = [[QPushButton(f"{self.lang_dict['search']}")],
                           [QPushButton(f"{self.lang_dict['add_prod']}"), self.on_add_prod],
                           [QPushButton(f"{self.lang_dict['rem_prod']}")],
                           [QPushButton(f"{self.lang_dict['finish']}")]]
                
            for w in widgets:
                val[0].addWidget(w[0])

                if len(w) > 1:
                    if isinstance(w[0], QPushButton):
                        w[0].clicked.connect(w[1]) # type: ignore
                
            val.append(widgets)
            
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        
        self.__init_vars__()

    
    # Variáveis
    def __init_vars__(self):
        self.cents_total = 0
        self.price_label = self.layouts["pay_price"][1][1][0]

    # Adicionar produto na transação
    def on_add_prod(self):
        prod_id = front_utils.ask_input(self.lang_dict["ask_id_desc"], self.lang_dict["ask_id_title"], input_type=int)
        quanitity = front_utils.ask_input(self.lang_dict["ask_quantity_desc"], self.lang_dict["ask_quantity_title"], input_type=int)        
        
        # Checa se o input não é vazio, se não for, continua
        if prod_id != "" and quanitity != "":
            try:
                transaction = self.backend.sell(int(prod_id), int(quanitity))
            except exceptions.ProdNotFoundException:
                front_utils.message(2, f"{self.lang_dict['prod_not_found']} {prod_id}")
                return
            
            # Adicionar a tabela
            table = self.layouts["transaction"][1][0]
            
            model = table[2]
            row_num = model.rowCount()
            column_num = model.columnCount()
            
            # Conseguir a proxima linha
            row = 0
            for row in range(row_num):
                if model.data(model.index(row, 0)) is None or model.data(model.index(row, 0)) == "":
                    break
            
            
            # Adicionar na linha a transação
            data = [transaction["prod_id"], transaction["name"], transaction["quantity"], finances.cents_to_money(transaction["total_sold"], self.config["money_unit"], self.config["decimal_place"], self.config["separator"])]
            for col in range(column_num):
                model.setData(model.index(row, col), data[col])
                
            
            # Adicionar ao valor
            self.cents_total += int(transaction["total_sold"])
            
            self.price_label.setText(finances.cents_to_money(self.cents_total, self.config["money_unit"], self.config["decimal_place"], self.config["separator"]))
            