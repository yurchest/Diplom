from experta import *
from pandas import DataFrame

from database import getRulesFromDb
from boolean_parser import parse


# class KE(KnowledgeEngine):
#     pass


def make_rule_decorator(lhs: str) -> list:
    logic_to_check = ['>', '<', '>=', '<=', '=']
    rules_validated = []
    lhs_splitted = lhs.split('&')
    for rule in lhs_splitted:
        if any(log in rule for log in logic_to_check):
            rule_parsed = parse(rule)
            if rule_parsed.operator == '=':
                rule_parsed.operator = '=='
            exec(f"rules_validated.append(Fact({rule_parsed.name} = P(lambda {rule_parsed.name}: {rule_parsed})))")
    return rules_validated


def make_func(rules_validated: list, fact_to_add: str, postcondition: str, priority: int) -> Rule:
    def func(self):
        if '=' in fact_to_add:
            exec(f"self.declare(Fact({fact_to_add}))")
        else:
            exec(f"self.declare(Fact('{fact_to_add}'))")
        if postcondition:
            exec(f"self.declare(Fact(action = '{postcondition}'))")

    return Rule(AND(*tuple(rules_validated)), salience=priority)(func)


def addRules(productions: DataFrame, ex) -> None:
    for ind in productions.index:
        rules_validated = make_rule_decorator(productions['lhs'][ind])
        setattr(ex, f"_{ind}", make_func(rules_validated, productions['rhs'][ind], productions['action'][ind], productions['priority'][ind]))


def declare_facts(facts: list[str], engine):
    for fact_to_add in facts:
        if '=' in fact_to_add:
            exec(f"engine.declare(Fact({fact_to_add}))")
        else:
            exec(f"engine.declare(Fact('{fact_to_add}'))")


if __name__ == '__main__':
    KE = type("KE", (KnowledgeEngine,), dict())
    addRules(getRulesFromDb("test_db.db", "test"), KE)
    engine = KE()
    engine.reset()
    engine.declare(Fact(temp=150, pressure=18))



    engine.run()
    print(engine.facts)
