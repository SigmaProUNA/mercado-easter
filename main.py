import market_frontend
import sys
from PyQt6.QtWidgets import QApplication
import json


def main():
    app = QApplication(sys.argv)
    window = market_frontend.MarketWindow("config.json")
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
