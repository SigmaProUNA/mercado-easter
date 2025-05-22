import market_backend
from PyQt6.QtWidgets import QMainWindow, QLabel


# Front end
class MarketWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easter")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height
        
        self.label = QLabel("Hoy!", self)
        self.label.move(150, 140) 

