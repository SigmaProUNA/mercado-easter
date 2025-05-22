import market_frontend
import sys
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = market_frontend.MarketWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
