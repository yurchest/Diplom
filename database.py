import os
import sys

import pandas as pd
import sqlite3

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox


def getRulesFromDb(db_name, tablename):
    try:
        sqliteConnection = sqlite3.connect(db_name)
        print("Database Successfully Connected to SQLite")
        df = pd.read_sql_query(f"SELECT * FROM {tablename}", sqliteConnection)
        return df
    except sqlite3.Error as error:
        msgBox = QMessageBox()
        msgBox.setText(f"Ошибка подключения к БД : \n {error}")
        msgBox.exec()
        sys.exit()
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def connect_QSQL_db(db_name):
    db = QSqlDatabase.addDatabase("QSQLITE")
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), db_name)
    db.setDatabaseName(file)
    if not db.open():
        msgBox = QMessageBox()
        msgBox.setText("Ошибка подключения к БД")
        msgBox.exec()
    else:
        return db
