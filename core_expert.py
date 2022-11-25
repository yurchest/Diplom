from experta import *
from pandas import DataFrame

from database import getRulesFromDb
from boolean_parser import parse


class KE(KnowledgeEngine):
    @DefFacts()
    def init_data(self):
        yield Fact(temp=150)
        yield Fact(pressure=18)


def make_rule_decorator(lhs: str) -> list:
    logic_to_check = ['>', '<', '>=', '<=', '=']
    rules_validated = []
    lhs_splitted = lhs.split('&')
    for rule in lhs_splitted:
        if any(log in rule for log in logic_to_check):
            rule_parsed = parse(rule)
            if rule_parsed.operator == '=':
                rule_parsed.operator = '=='
            exec(f"rules_validated.append(Fact({rule_parsed.name} = P(lambda {rule_parsed.name}: {rule})))")
    return rules_validated


def make_func(rules_validated: list, fact_to_add: str, postcondition: str) -> Rule:
    def func(self):
        if '=' in fact_to_add:
            exec(f"self.declare(Fact({fact_to_add}))")
        else:
            exec(f"self.declare(Fact('{fact_to_add}'))")
        if postcondition:
            print(postcondition)
    return Rule(AND(*tuple(rules_validated)))(func)


def addRules(productions: DataFrame) -> None:
    for ind in productions.index:
        rules_validated = make_rule_decorator(productions['lhs'][ind])
        setattr(KE, f"_{ind}", make_func(rules_validated, productions['rhs'][ind], productions['postcondition'][ind]))


addRules(getRulesFromDb())
engine = KE()
engine.reset()
# engine.declare(Fact(temp=150, pressure=18))
engine.run()
print(engine.facts)