import re


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
