from PyQt6.QtWidgets import QWidget

from Models.production_base import ProdBaseModel
from UI.new_form import *
from Widgets.edit_facts import EditFacts
from src.core_expert2 import *
from src.utils import *


class App(QWidget):
    tablename = "test"

    def __init__(self):
        QWidget.__init__(self)
        self.w = QtWidgets.QMainWindow()
        self.w_root = Ui_MainWindow()
        self.w_root.setupUi(self.w)

        # self.init_data_form = InitData(self)
        self.db, self.db_filename = connect_knowledge_base()
        self.engine = self.init_engine()

        self.edit_facts_form = EditFacts(self.db, self.engine, self.w_root.tableWidget)

        self.base_model = ProdBaseModel(self.db, self.tablename)
        self.w_root.tableView.setModel(self.base_model)
        self.w_root.tableView.resizeColumnsToContents()
        # TODO сделать изменяемым

        self.w_root.pushButton.clicked.connect(self.edit_facts)
        self.w_root.pushButton_2.clicked.connect(self.solve)

        self.w.show()

    def edit_facts(self):
        self.w_root.tableWidget.clearContents()
        self.w_root.tableWidget.setRowCount(0)
        self.edit_facts_form.w.show()

    def init_engine(self):
        KE = type("KE", (KnowledgeEngine,), dict())
        self.df_rules = getRulesFromDb(self.db_filename, self.tablename)
        addRules(
            productions=self.df_rules,
            ex=KE,
            description_text_browser=self.w_root.textBrowser,
            work_memory_table_widget=self.w_root.tableWidget_2,
        )
        engine = KE()
        engine.reset()
        return engine


    def solve(self):
        self.w_root.tableWidget_2.clearContents()
        self.w_root.tableWidget_2.setRowCount(0)
        # user_declare_facts(["температура=40", "кашель=true", "насморк=true"], self.engine)
        self.engine.run()
        print(self.engine.facts)
        # self.update_work_memory()
