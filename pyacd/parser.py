"""
  parser module for EMBOSS ACD files
"""
from .acd import get_parameter, Attribute, Section, Application, Acd, PARAMETER_CLASSES
from pyparsing import Word, QuotedString, Group, ZeroOrMore, oneOf, Suppress, restOfLine, alphanums

NAME = Word(alphanums)
VALUE = QuotedString('"', multiline=True)

ATTRIBUTE = NAME('name') + Suppress(':') + VALUE('value')
def _get_attribute(tokens):
    """ return Attribute object from tokens """
    return Attribute(name=tokens['name'], value=tokens.get('value', ''))
ATTRIBUTE.setParseAction(_get_attribute)
ATTRIBUTES_LIST = Group(ZeroOrMore(ATTRIBUTE)).setResultsName('attributes')

DATATYPE = oneOf(PARAMETER_CLASSES.keys())
PARAMETER = Group(DATATYPE('datatype') + Suppress(":") + NAME('name') + Suppress("[") +
                  ATTRIBUTES_LIST('properties') + Suppress("]"))
def _get_parameter(tokens):
    """ return Parameter object from tokens """
    token = tokens[0]
    return get_parameter(token['name'], token['datatype'], token['properties'])
PARAMETER.setParseAction(_get_parameter)
PARAMETERS_LIST = Group(ZeroOrMore(PARAMETER)).setResultsName('parameters')

SECTION = Group(
    Suppress("section:") + NAME('name') + Suppress("[")
    + ATTRIBUTES_LIST('properties') + Suppress("]") + \
    PARAMETERS_LIST('parameters') + Suppress("endsection:") + Suppress(NAME))
def _get_section(tokens):
    """ return Section object from tokens """
    token = tokens[0]
    return Section(token['name'], properties=token['properties'],
                   parameters=token['parameters'])
SECTION.setParseAction(_get_section)
SECTIONS_LIST = Group(ZeroOrMore(SECTION))

APPLICATION = Suppress("application") + ":" + NAME('name') + Suppress("[") \
              + ATTRIBUTES_LIST('properties') + Suppress("]")
def _get_application(tokens):
    """ return Application object from tokens """
    return Application(tokens['name'], attributes=tokens['properties'])
APPLICATION.setParseAction(_get_application)

ACD = APPLICATION('application') + SECTIONS_LIST('sections')
# ignore ACD comments (starting with a '#')
ACD.ignore("#" + restOfLine)
def _get_acd(token):
    """ return Acd object from tokens """
    return Acd(token['application'], token['sections'])
ACD.setParseAction(_get_acd)

def parse_attribute(string):
    """ parse ACD attribute """
    return ATTRIBUTE.parseString(string)[0]

def parse_attributes(string):
    """ parse ACD attributes list """
    results = ATTRIBUTES_LIST.parseString(string)[0]
    return [item for item in results]

def parse_parameter(string):
    """ parse parameter """
    return PARAMETER.parseString(string)[0]

def parse_parameters(string):
    """ parse parameters list """
    results = PARAMETERS_LIST.parseString(string)[0]
    return [item for item in results]

def parse_application(string):
    """ parse application """
    return APPLICATION.parseString(string)[0]

def parse_section(string):
    """ parse section """
    return SECTION.parseString(string)[0]

def parse_sections(string):
    """ parse sections list """
    results = SECTIONS_LIST.parseString(string)[0]
    return [item for item in results]

def parse_acd(string):
    """ parse Acd """
    return ACD.parseString(string)[0]
