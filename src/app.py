from PyQt6.QtWidgets import QWidget, QFileDialog
from UI.form import *
from Models.production_base import ProdBaseModel
from src.database import connect_QSQL_db
from Widgets.init_data import InitData

from src.core_experta2 import *


class App(QWidget):
    tablename = "test"

    def __init__(self):
        QWidget.__init__(self)
        self.w = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.w)

        self.init_data_form = InitData(self)
        self.w_root.pushButton_2.setEnabled(False)
        self.w_root.pushButton_3.setEnabled(False)

        self.w_root.pushButton.clicked.connect(self.download_base)
        self.w_root.pushButton_3.clicked.connect(self.init_data)
        self.w_root.pushButton_2.clicked.connect(self.solve)

        self.w.show()

    def download_base(self):
        filename, _ = QFileDialog.getOpenFileName(None, 'Open Base', './', "Database (*.db *.sqlite *.sqlite3)")
        self.db = connect_QSQL_db(filename)
        if self.db:
            self.base_model = ProdBaseModel(self.db, self.tablename)
            self.w_root.tableView.setModel(self.base_model)
            self.resize_columns()
            # self.w_root.tableView.horizontalHeader().moveSection(5, 3)
            # self.w_root.tableView.horizontalHeader().moveSection(6, 4)
            self.db.close()
            self.df_rules = getRulesFromDb(filename, self.tablename)
            self.w_root.pushButton_2.setEnabled(True)
            self.w_root.pushButton_3.setEnabled(True)
            KE = type("KE", (KnowledgeEngine,), dict())
            addRules(self.df_rules, KE)
            self.engine = KE()
            self.engine.reset()
            print(self.df_rules)

    def init_data(self):
        self.init_data_form.w.show()
        # self.update_work_memory()

    def solve(self):
        self.engine.run()
        self.update_work_memory()

    def update_work_memory(self):
        facts = []
        for i in range(1, len(self.engine.facts)):
            key = str(list(self.engine.facts[i].as_dict().keys())[0])
            value = str(list(self.engine.facts[i].as_dict().values())[0])
            if key != "0":
                k_value = f"{key} = {value} \t\t"
                facts.append(f"{k_value}")
            else:
                facts.append(value)
        self.w_root.textBrowser.clear()
        self.w_root.textBrowser.setText("\n".join(facts))

    def resize_columns(self):
        # for i in range(6):
        #     self.w_root.tableView.resizeColumnToContents(i)
        #     self.w_root.tableView.setColumnWidth(i, self.w_root.tableView.columnWidth(i) + 10)
        self.w_root.tableView.setColumnWidth(0, 100)
        self.w_root.tableView.setColumnWidth(1, 400)
        self.w_root.tableView.setColumnWidth(2, 350)
        self.w_root.tableView.setColumnWidth(3, 100)