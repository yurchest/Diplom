import sys
from PyQt6.QtWidgets import QApplication
from src.app2 import App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    app.exec()
