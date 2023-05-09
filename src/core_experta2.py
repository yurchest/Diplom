from experta import *
from pandas import DataFrame
from src.database import getRulesFromDb

from src.utils import parse_expression


def make_rule_decorator(lhs: str) -> list:
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


def make_func(rules_validated: list, fact_to_add: str, priority: int) -> Rule:
    def func(self):
        if fact_to_add:
            self.declare(make_fact(fact_to_add))

    return Rule(AND(*tuple(rules_validated)), salience=priority)(func)


def addRules(productions: DataFrame, ex: KnowledgeEngine) -> None:
    for ind in productions.index:
        rules_validated = make_rule_decorator(productions['lhs'][ind])
        setattr(ex, f"_{ind}", make_func(rules_validated, productions['rhs'][ind], productions['priority'][ind]))


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


def user_declare_facts(facts: list[str], engine):
    print(facts)
    for fact_to_add in facts:
        if fact_to_add:
            engine.declare(make_fact(fact_to_add))


if __name__ == '__main__':
    KE = type("KE", (KnowledgeEngine,), dict())
    addRules(getRulesFromDb("../test_db_3.db", "test"), KE)
    engine = KE()
    engine.reset()
    engine.declare(Fact(temperature=10, rain='no', time="evening"))

    engine.run()
    print(engine.facts)
