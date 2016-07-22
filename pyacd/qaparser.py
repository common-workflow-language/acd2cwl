"""
  parser module for EMBOSS QA files
"""
from pyparsing import Optional, Suppress, Word, OneOrMore, ZeroOrMore, \
    printables, Group, alphanums, alphas

CL_PARAMETER = Optional((Suppress('--') | Suppress('-')) + Word(
    alphas)('name')) + Word(printables)('value')
CL_PARAMETERS = OneOrMore(Group(CL_PARAMETER(
    'parameter')))('parameters')
FILE_GROUP = Suppress("FI") + Word(printables)('file') \
             + Optional(Suppress("FC") + Word(printables)('linecount')) \
             + ZeroOrMore(Suppress("FP") + Word(printables)('pattern'))
QA = Suppress("ID") + Word(alphanums + '-')('id') + Suppress(
    "AP") + Word(alphas)('application') \
     + Suppress("CL") + CL_PARAMETERS('commandline') \
     + ZeroOrMore(Group(FILE_GROUP)('file'))('files')


def parse_cl_parameter(string):
    """ parse a parameter in a CL line """
    return CL_PARAMETER.parseString(string)

def parse_cl_parameters(string):
    """ parse a group of parameters in a CL line"""
    return CL_PARAMETERS.parseString(string)

def parse_qa(string):
    """ parse a QA test item (one test case for one application)"""
    return QA.parseString(string)
