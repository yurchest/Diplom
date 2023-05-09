from PyQt6.QtWidgets import QWidget

from Models.production_base import ProdBaseModel
from UI.new_form import *
from Widgets.edit_facts import EditFacts
# from src.core_experta2 import *
from src.utils import *


class App(QWidget):
    tablename = "test"

    def __init__(self):
        QWidget.__init__(self)
        self.w = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.w)

        # self.init_data_form = InitData(self)

        self.db = connect_knowledge_base()
        self.edit_facts_form = EditFacts(self.db)

        self.base_model = ProdBaseModel(self.db, self.tablename)
        self.w_root.tableView.setModel(self.base_model)
        # TODO сделать изменяемым

        self.w_root.pushButton.clicked.connect(self.edit_facts)

        self.w.show()

    def edit_facts(self):
        self.edit_facts_form.w.show()

    def download_base(self):
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
