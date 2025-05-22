import market_backend
from PyQt6.QtWidgets import QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QTableView
from PyQt6.QtCore import Qt


# Front end
class MarketWindow(QMainWindow):
    def __init__(self, config: dict):
        super().__init__()
        self.setWindowTitle("Easter")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height
        
        # Configurações
        self.config = config
        self.lang_dict = self.config["words"][self.config["selected_lang"]]
        
        # Widget central
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Layouts para a UI
        self.layouts = {
            "top_bar": QHBoxLayout(),
            "pay_price": QVBoxLayout(),
            "transaction": QHBoxLayout(),
            "bottom_bar": QHBoxLayout()
        }
        
        # Adicionar no central e já ir colocando widgets
        for key, val in self.layouts.items():
            self.main_layout.addLayout(val)
            
            # Lista de widgets
            widgets = []
            
            if key == "top_bar":
                widgets = [QLabel("Easter"),
                QPushButton(f"{self.lang_dict['gen_report']}"),
                QPushButton(f"{self.lang_dict['db_edit']}")]
            elif key == "pay_price":
                widgets = [
                    QLabel(f"{self.lang_dict['total_sold']}:"),
                    QLabel("0")
                ]
            elif key == "transaction":
                widgets = [QTableView()]
            elif key == "bottom_bar":
                widgets = [QPushButton(f"{self.lang_dict['search']}"),
                           QPushButton(f"{self.lang_dict['add_prod']}"),
                           QPushButton(f"{self.lang_dict['rem_prod']}"),
                           QPushButton(f"{self.lang_dict['finish']}")]
                
            for w in widgets:
                val.addWidget(w)
            
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

