from PyQt6.QtSql import *
from PyQt6.QtCore import Qt


class ProdBaseModel(QSqlQueryModel):
    header_data = {"date": "Дата",
                   "lhs": "Условие",
                   "support": "Поддержка",
                   "rhs": "Постусловие",
                   "probability": "Уверенность \nвыполнения",
                   "proportion": "Доля \nнаблюдений",
                   "priority": "Приоритет",
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
        self.setQuery(f"""SELECT * FROM {self.tablename}""")
