from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QFormLayout, QPushButton, QLabel, QVBoxLayout, QGroupBox, QComboBox, \
    QLineEdit
from UI.edit_facts import *
from Models.facts import Facts
from src.core_expert2 import *


class EditFacts(QWidget):
    def __init__(self, db, engine, facts_table_widget):
        QWidget.__init__(self)
        self.w = QtWidgets.QDialog()
        self.w_root = Ui_Dialog()
        self.w_root.setupUi(self.w)
        # TODO ALL
        self.db = db
        self.engine = engine
        self.facts_table_widget = facts_table_widget

        self.facts_model = Facts(self.db, "facts")
        self.w_root.tableView.setModel(self.facts_model)
        self.w_root.tableView.resizeColumnsToContents()

        self.add_fact_button = QPushButton("Добавить")

        self.add_fact_button.clicked.connect(self.add_fact)
        self.w_root.pushButton.clicked.connect(lambda: self.apply(add=True))
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

    def apply(self, add=True):
        facts_to_add = []
        # iterate over formLayout rows
        for row in range(self.formLayout.rowCount() - 1):
            fact_name = self.formLayout.itemAt(row, QFormLayout.ItemRole.LabelRole).widget().currentText()
            fact_value = self.formLayout.itemAt(row, QFormLayout.ItemRole.FieldRole).widget().text()
            if fact_value:
                fact = f"{fact_name}={fact_value}"
            else:
                fact = fact_name

            facts_to_add.append(fact)
            if add:
                rowPosition = self.facts_table_widget.rowCount()
                self.facts_table_widget.insertRow(rowPosition)
                self.facts_table_widget.setItem(rowPosition, 0, QTableWidgetItem(fact_name))
                self.facts_table_widget.setItem(rowPosition, 1, QTableWidgetItem(fact_value))

        try:
            user_declare_facts(facts_to_add, self.engine)
            self.w.close()
        except TypeError:
            msgBox = QMessageBox()
            msgBox.setText("Факты заданы неверно.")
            msgBox.exec()
