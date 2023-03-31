from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox
from UI.init_data import Ui_Form

from src.core_experta2 import user_declare_facts


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
        self._add_facts(facts.split("\n"))
        self.w.close()
        self.main_app.update_work_memory()

    def _add_facts(self, facts: list[str]):
        try:
            user_declare_facts(facts, self.main_app.engine)
            self.main_app.w_root.textBrowser_2.setText("\n".join(facts))
        except (SyntaxError):
            self.main_app.engine.reset()
            self.main_app.w_root.textBrowser_2.clear()
            self.main_app.update_work_memory()
            msgBox = QMessageBox()
            msgBox.setText("Ошибка добавления фактов")
            msgBox.exec()

            # raise SyntaxError
