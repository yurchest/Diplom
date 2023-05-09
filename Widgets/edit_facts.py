from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox
from UI.edit_facts import *
from Models.facts import Facts


class EditFacts(QWidget):
    def __init__(self, db):
        QWidget.__init__(self)
        self.w = QtWidgets.QDialog()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self.w)
        # TODO ALL
        self.db = db

        self.facts_model = Facts(self.db, "facts")
        self.w_root.tableView.setModel(self.facts_model)


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
