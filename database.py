import pandas as pd
import sqlite3

def getRulesFromDb():
    try:
        sqliteConnection = sqlite3.connect('test_db.db')
        cursor = sqliteConnection.cursor()
        print("Database Successfully Connected to SQLite")
        sqlite_select_Query = "SELECT * FROM test"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        df = pd.read_sql_query("SELECT * FROM test", sqliteConnection)
        print(df)
        cursor.close()
        return df
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

