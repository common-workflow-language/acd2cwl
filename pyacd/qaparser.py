from pyparsing import Optional, Suppress, Word, OneOrMore, ZeroOrMore, \
    printables, Group, alphanums, alphas

cl_parameter = Optional((Suppress('--') | Suppress('-')) + Word(
    alphas)('name')) + Word(printables)('value')
cl_parameters = OneOrMore(Group(cl_parameter(
    'parameter')))('parameters')
file_group = Suppress("FI") + Word(printables)('file') \
                  + Optional(Suppress("FC") + Word(printables)('linecount')) \
                  + ZeroOrMore(Suppress("FP") + Word(printables)('pattern'))
qa = Suppress("ID") + Word(alphanums + '-')('id') + Suppress(
    "AP") + Word(alphas)('application') \
            + Suppress("CL") + cl_parameters('commandline') \
            + ZeroOrMore(Group(file_group)('file'))('files')


def parse_cl_parameter(string):
    return cl_parameter.parseString(string)


def parse_cl_parameters(string):
    return cl_parameters.parseString(string)

def parse_qa(string):
    return qa.parseString(string)