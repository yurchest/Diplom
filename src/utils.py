import re
import os
import sys

import pandas as pd
import sqlite3

from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QMessageBox, QFileDialog


def parse_expression(expression):
    # Список допустимых операторов сравнения
    operators = ['>=', '<=', '<', '==', '!=', '>', '=']
    expression = expression.replace(' ', '')
    # Проверка наличия скобок в строке
    if expression.startswith("(") and expression.endswith(")"):
        expression = expression[1:-1]

    # Поиск оператора сравнения в строке
    for op in operators:
        if op in expression:
            operator = op
            break
    else:
        return 0

    # Разбиение строки на переменную и значение
    variable, value = expression.split(operator)
    variable = variable.strip()
    value = str_to_num(value.strip())

    return variable, operator, value


def is_number(s):
    if isinstance(s, str):
        return bool(re.match("^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$", s))
    return False


def str_to_num(s):
    if is_number(s):
        try:
            return float(s)
        except ValueError:
            return s
    else:
        return s


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


def connect_knowledge_base():
    filename, _ = QFileDialog.getOpenFileName(None, 'Open Base', './', "Database (*.db *.sqlite *.sqlite3)")
    db = connect_QSQL_db(filename)
    return db
