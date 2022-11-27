from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox
from UI.init_data import Ui_Form

from core_expert import declare_facts

class InitData(QWidget):
    def __init__(self, main_app):
        QWidget.__init__(self)
        self.w = QtWidgets.QDialog()
        self.w_root = Ui_Form()
        self.w_root.setupUi(self.w)

        self.main_app = main_app


        self.w_root.pushButton_2.clicked.connect(lambda: self.w.close())
        self.w_root.pushButton.clicked.connect(self.__accept)

    def __accept(self):
        self.main_app.engine.reset()
        facts = self.w_root.textEdit.toPlainText()
        # try:
        declare_facts(facts.split("\n"), self.main_app.engine)
        self.w.close()
        self.main_app.w_root.textBrowser_2.setText(facts)
        self.main_app.update_work_memory()
        # except:
        #     msgBox = QMessageBox()
        #     msgBox.setText("Ошибка добавления фактов")
        #     msgBox.exec()


