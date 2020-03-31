import pyparsing as pp


class OrCondition(object):
    def __init__(self, tokens):
        self.terms = [x for x in tokens if not isinstance(x, str)]


class AndCondition(object):
    def __init__(self, tokens):
        self.terms = [x for x in tokens if not isinstance(x, str)]


class NotCondition(object):
    def __init__(self, tokens):
        if len(tokens) == 1:
            self.negated = False
            self.condition = tokens[0]
        else:
            self.negated = True
            self.condition = tokens[1]


class Condition(object):
    def __init__(self, tokens):
        self.identifier = tokens[0]
        self.args = [x.number for x in tokens[1:]]
        pass


class Number(object):
    def __init__(self, nums):
        self.number = int(nums[0])


class Identifier(object):
    def __init__(self, name):
        self.name = name


def language_def(self):
    and_ = pp.CaselessLiteral("and")
    or_ = pp.CaselessLiteral("or")
    not_ = pp.CaselessLiteral("not")
    number = (pp.Word(pp.nums)).setParseAction(Number)
    functionname = pp.Word(pp.alphanums + '_').setParseAction(Identifier)
    functionbody = pp.Forward()
    functionbody <<=  functionname + (pp.Suppress("(") +
                                      pp.Optional(pp.delimitedList(number),'')
                                      + pp.Suppress(")"))
    condition = functionbody | functionname
    condition.setParseAction(Condition)
    not_condition = (not_ + condition | condition).setParseAction(NotCondition)
    and_condition = (not_condition + pp.ZeroOrMore(and_ + not_condition)).setParseAction(AndCondition)
    or_condition = (and_condition + pp.ZeroOrMore(or_ + and_condition)).setParseAction(OrCondition)
    expression = or_condition
    return expression


ROBO_LANGUAGE = language_def()

