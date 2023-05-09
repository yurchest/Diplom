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

    def __change_column_name(self):
        for i in range(self.columnCount()):
            self.setHeaderData(i, Qt.Orientation.Horizontal, self.header_data[self.record().fieldName(i)])

    def __update(self):
        self.setQuery(f"""SELECT fact, min_num, max_num, step_num_variants_text FROM {self.tablename}""")