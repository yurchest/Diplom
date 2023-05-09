""""

1. Таблица со всеми возможными фактами на объекте и их
2. Вывести список фактов
3. UI для выбора факта из выпадающего окна (домены к фактам)
4. Изменять базу знаний
5. В БЗ должны быть факты на добавление и действия отдельно

"""
from PyQt6.QtWidgets import QTextBrowser
from experta import *
from pandas import DataFrame

from src.utils import parse_expression


def get_rules_validated(lhs: str) -> list:
    rules_validated = []
    lhs_splitted = lhs.split('&')

    for rule in lhs_splitted:
        parsed_result = parse_expression(rule)
        print(parsed_result)
        if parsed_result:
            variable, operator, value = parsed_result
            if operator == "=":
                operator = "=="
            if isinstance(value, str):
                fact = eval(f"Fact({variable} = P(lambda {variable}: {variable} {operator} '{value}'))")
            else:
                fact = eval(f"Fact({variable} = P(lambda {variable}: {variable} {operator} {value}))")
        else:
            fact = eval(f"Fact({rule})")

        rules_validated.append(fact)

    return rules_validated


def make_fact(fact_not_parsed: str) -> Fact:
    parsed_result = parse_expression(fact_not_parsed)
    if parsed_result[1] != "=":
        raise TypeError
    if parsed_result:
        variable, operator, value = parsed_result
        if isinstance(value, str):
            fact = eval(f"Fact({variable} = '{value}')")
        else:
            fact = eval(f"Fact({variable} = {value})")
    else:
        fact = eval(f"Fact('{fact_not_parsed}')")
    return fact


def make_func(rules_validated: list,
              fact_to_add: str,
              priority: int,
              description: str,
              description_text_browser: QTextBrowser,
              work_memory_text_browser: QTextBrowser,
              ) -> Rule:
    def func(self):
        if fact_to_add:
            self.declare(make_fact(fact_to_add))
            work_memory_text_browser.setText(fact_to_add + "\n")
        if description:
            description_text_browser.setText(description + "\n")

    return Rule(AND(*tuple(rules_validated)), salience=priority)(func)


def addRules(productions: DataFrame,
             ex: KnowledgeEngine,
             description_text_browser: QTextBrowser,
             work_memory_text_browser: QTextBrowser,
             ) -> None:
    for ind in productions.index:
        rules_validated = get_rules_validated(productions['lhs'][ind])
        setattr(ex, f"_{ind}",
                make_func(
                    rules_validated=rules_validated,
                    fact_to_add=productions['fact_to_add'][ind],
                    priority=productions['priority'][ind],
                    description=productions['description'][ind],
                    description_text_browser=description_text_browser,
                    work_memory_text_browser=work_memory_text_browser,
                ), )
