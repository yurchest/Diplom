from experta import *
from pandas import DataFrame

from database import getRulesFromDb
from boolean_parser import parse


# class KE(KnowledgeEngine):
#     pass


def make_rule_decorator(lhs: str, support: str) -> list:
    logic_to_check = ['>', '<', '>=', '<=', '=']
    rules_validated = []
    support_splitted = support.split(";")
    # print(lhs)
    lhs_splitted = lhs.split('&')
    for rule, sup in zip(lhs_splitted, support_splitted):

        if any(log in rule for log in logic_to_check):
            rule_parsed = parse(rule)
            if rule_parsed.operator == '=':
                rule_parsed.operator = '=='
            try:
                num = float(rule_parsed.value)
                exec(f"rules_validated.append(Fact({rule_parsed.name} = P(lambda {rule_parsed.name}: {rule_parsed})))")
            except ValueError:
                exec(f"rules_validated.append(Fact({rule_parsed.name} = P(lambda {rule_parsed.name}: {rule_parsed.name} == '{rule_parsed.value}')))")
            exec(
                f"rules_validated.append(Fact({rule_parsed.name}_support_ = P(lambda {rule_parsed.name}_support_: {rule_parsed.name}_support_ > {sup})))")

        else:
            exec(f"rules_validated.append(Fact('{rule}'))")
            exec(
                f"rules_validated.append(Fact({rule}_support_ = P(lambda {rule}_support_: {rule}_support_ > {sup})))")
    return rules_validated


def make_func(rules_validated: list, fact_to_add: str, probability: float, priority: int) -> Rule:
    def func(self):
        if '=' in fact_to_add:
            fact_to_add_parsed = parse(fact_to_add)
            print(fact_to_add_parsed)
            try:
                num = float(fact_to_add_parsed.value)
                exec(f"self.declare(Fact({fact_to_add_parsed.name} = {num}))")
            except ValueError:
                print(f"self.declare(Fact({fact_to_add_parsed.name}='{fact_to_add_parsed.value}'))")
                exec(f"self.declare(Fact({fact_to_add_parsed.name}='{fact_to_add_parsed.value}'))")

            fact_to_add__support = fact_to_add.split("=")[0].strip() + "_support_=" + str(probability)
        else:
            exec(f"self.declare(Fact('{fact_to_add}'))")
            fact_to_add__support = fact_to_add + "_support_=" + str(probability)
        exec(f"self.declare(Fact({fact_to_add__support}))")

    return Rule(AND(*tuple(rules_validated)), salience=priority)(func)


def addRules(productions: DataFrame, ex) -> None:
    for ind in productions.index:
        rules_validated = make_rule_decorator(productions['lhs'][ind], productions['support'][ind])
        setattr(ex, f"_{ind}", make_func(rules_validated, productions['rhs'][ind], productions['probability'][ind],
                                         productions['priority'][ind]))


def declare_facts(facts: list[str], engine, support=1.0):
    for fact_to_add in facts:
        if '=' in fact_to_add:
            fact_to_add_parsed = parse(fact_to_add)
            print(fact_to_add_parsed)
            try:
                num = float(fact_to_add_parsed.value)
                exec(f"engine.declare(Fact({fact_to_add_parsed.name} = {num}))")
            except ValueError:
                print(f"engine.declare(Fact({fact_to_add_parsed.name}='{fact_to_add_parsed.value}'))")
                exec(f"engine.declare(Fact({fact_to_add_parsed.name}='{fact_to_add_parsed.value}'))")


            fact_to_add__support = fact_to_add.split("=")[0].strip() + "_support_=" + str(support)
        else:
            exec(f"engine.declare(Fact('{fact_to_add}'))")
            fact_to_add__support = fact_to_add.strip() + "_support_=" + str(support)
        exec(f"engine.declare(Fact({fact_to_add__support}))")


if __name__ == '__main__':
    KE = type("KE", (KnowledgeEngine,), dict())
    addRules(getRulesFromDb("test_db_2.db", "test"), KE)
    engine = KE()
    engine.reset()
    try:
        engine.modify(Fact(temperature=-10, pressure=18))
    except IndexError:
        engine.declare(Fact(temperature=-10, pressure=18))


    engine.run()
    print(engine.facts)
