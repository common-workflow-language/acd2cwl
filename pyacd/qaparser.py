from pyparsing import *


class QAParser(object):
    def __init__(self):
        self.cl_parameter = Optional((Suppress('--')|Suppress('-')) + Word(alphas)('name')) + Word(printables)('value')
        self.cl_parameters = OneOrMore(Group(self.cl_parameter('parameter')))('parameters')
        self.fileGroup = Suppress("FI") + Word(printables)('file') \
                    + Optional(Suppress("FC") + Word(printables)('linecount')) \
                    + ZeroOrMore(Suppress("FP") + Word(printables)('pattern'))
        self.test = Suppress("ID") + Word(alphanums+'-')('id') + Suppress("AP") + Word(alphas)('application') \
                    + Suppress("CL") + self.cl_parameters('commandline') \
                    + ZeroOrMore(Group(self.fileGroup)('file'))('files')

    def parse_cl_parameter(self, string):
        return self.cl_parameter.parseString(string)

    def parse_cl_parameters(self, string):
        return self.cl_parameters.parseString(string)

    def parse_test(self, string):
        return self.test.parseString(string)
