from experta import *
import sqlite3
from boolean_parser import parse
import pandas as pd


def getRulesFromDb():
    try:
        sqliteConnection = sqlite3.connect('test_db.db')
        cursor = sqliteConnection.cursor()
        print("Database Successfully Connected to SQLite")
        sqlite_select_Query = "SELECT * FROM test"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        # df = pd.read_sql_query("SELECT * FROM test", sqliteConnection)
        # print(df)
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def addRules(rules: dict):
    for k in rules.keys():
        facts_validated = []
        if ';' in k:
            key_rule_splitted = k.split(';')
''
            for rule in key_rule_splitted:
                logic_to_check = ['>', '<', '>=', '<=', '=']
                if any(log in rule for log in logic_to_check):
                    rule_splitted = parse(rule)
                    if rule_splitted.operator == '=':
                        rule_splitted.operator = '=='
                    exec(f"facts_validated.append(Fact({rule_splitted.name} = P(lambda {rule_splitted.name}: {rule})))")
                else:
                    exec(f"facts_validated.append(Fact('{rule}'))")

        else:
            exec(f"facts_validated.append(Fact('{k}'))")

        setattr(KE, rules[k], make_func(facts_validated, rules[k]))


def make_rule_decorator(lhs: str):
    logic_to_check = ['>', '<', '>=', '<=', '=']
    rules_validated = []
    if '&' in lhs:
        lhs_splitted = lhs.split('&')

        for rule in lhs_splitted:
            if any(log in rule for log in logic_to_check):
                rule_parsed = parse(rule)
                if rule_parsed.operator == '=':
                    rule_parsed.operator = '=='
                exec(f"rules_validated.append(Fact({rule_parsed.name} = P(lambda {rule_parsed.name}: {rule})))")


def make_func(facts_validated, fact_to_add):
    def func(self):
        if '=' in fact_to_add:
            exec(f"self.declare(Fact({fact_to_add}))")
        else:
            exec(f"self.declare(Fact('{fact_to_add}'))")

    return Rule(AND(*tuple(facts_validated)))(func)


class KE(KnowledgeEngine):
    @DefFacts()
    def init_data(self):
        yield Fact(temp=150)
        yield Fact(pressure=18)


def getDictData():
    knowlege_base = getRulesFromDb()
    rules = {}
    for record in knowlege_base:
        rules.update({record[1]: record[2]})
    print(rules)
    return rules


data = getDictData()
addRules(data)

engine = KE()
engine.reset()
# engine.declare(Fact(temp=150, pressure=18))
engine.run()
print(engine.facts)

