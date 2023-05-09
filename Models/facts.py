from PyQt6.QtSql import *
from PyQt6.QtCore import Qt


class Facts(QSqlQueryModel):
    header_data = {"fact": "Факт",
                   "type": "Тип данных",
                   "min_num": "Мин",
                   "max_num": "Макс",
                   "step_num": "Шаг",
                   "variants_text": "Варианты",
                   }

    def __init__(self, db, tablename):
        super().__init__()
        self.db = db
        self.tablename = tablename
        self.__update()
        self.__change_column_name()
        # self.test_query()

    def __change_column_name(self):
        for i in range(self.columnCount()):
            self.setHeaderData(i, Qt.Orientation.Horizontal, self.header_data[self.record().fieldName(i)])

    def __update(self):
        self.setQuery(f"""SELECT fact FROM {self.tablename}""")

    def test_query(self):
        query = QSqlQuery()
        query.exec(f"""SELECT fact FROM facts""")
        while query.next():
            print(query.value(0))

    def get_facts(self):
        facts = []
        query = QSqlQuery()
        query.exec(f"SELECT * FROM {self.tablename}")
        while query.next():
            facts.append({
                "fact": query.value(0),
                "type": query.value(1),
                "min_num": query.value(2),
                "max_num": query.value(3),
                "step_num": query.value(4),
                "variants_text": query.value(5),
            })
        return facts

    def get_list_facts(self):
        facts = set()
        query = QSqlQuery()
        query.exec(f"SELECT fact FROM {self.tablename}")
        while query.next():
            facts.add(query.value(0))
        return facts
