from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QFormLayout, QPushButton, QLabel, QVBoxLayout, QGroupBox, QComboBox, \
    QLineEdit
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

        self.add_fact_button = QPushButton("Добавить")

        self.add_fact_button.clicked.connect(self.add_fact)
        self.w_root.pushButton.clicked.connect(self.apply)
        self.w_root.pushButton_2.clicked.connect(lambda: self.w.close())

        self.facts = self.facts_model.get_list_facts()
        self.facts_add = self.facts_model.get_facts()
        self.init_scroll_area()

    def init_scroll_area(self):
        groupBox = QGroupBox()
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.add_fact_button)
        groupBox.setLayout(self.formLayout)
        self.w_root.scrollArea.setWidget(groupBox)

    def add_fact(self):
        comboBox = QComboBox()
        comboBox.addItems(self.facts)
        self.formLayout.insertRow(self.formLayout.rowCount() - 1, comboBox, QLineEdit())

    def layout_widgets(self, layout):
        return (layout.itemAt(i) for i in range(layout.count() - 1))

    def apply(self):
        pass
