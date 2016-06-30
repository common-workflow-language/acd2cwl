from .acd import getParameter, Attribute, Section, Application, Acd, PARAMETER_CLASSES
from pyparsing import *


class AcdParser(object):
    def __init__(self):
        self.name = Word(alphanums)
        self.value = QuotedString('"', multiline=True)

        self.attribute = self.name('name') + Suppress(':') + self.value('value')

        def get_attribute(t):
            return Attribute(name=t['name'], value=t.get('value', ''))

        self.attribute.setParseAction(get_attribute)

        self.attributes_list = Group(ZeroOrMore(self.attribute)).setResultsName('attributes')

        self.datatype = oneOf(PARAMETER_CLASSES.keys())
        self.parameter = Group(self.datatype('datatype') + Suppress(":") + self.name('name') + Suppress("[") +
                               self.attributes_list('properties') + Suppress("]"))

        def get_parameter(tokens):
            token = tokens[0]
            return getParameter(token['name'], token['datatype'], token['properties'])

        self.parameter.setParseAction(get_parameter)

        self.parameters_list = Group(ZeroOrMore(self.parameter)).setResultsName('parameters')

        self.section = Group(
            Suppress("section:") + self.name('name') + Suppress("[") + self.attributes_list('properties') + Suppress(
                "]") + \
            self.parameters_list('parameters') + Suppress("endsection:") + Suppress(self.name))

        def get_section(tokens):
            token = tokens[0]
            return Section(token['name'], properties=token['properties'], parameters=token['parameters'])

        self.section.setParseAction(get_section)
        self.sections_list = Group(ZeroOrMore(self.section))
        self.application = Suppress("application") + ":" + self.name('name') + Suppress("[") + self.attributes_list(
            'properties') + Suppress("]")

        def get_application(s, l, t):
            r = Application(t['name'], attributes=t['properties'])
            return r

        self.application.setParseAction(get_application)
        self.acd = self.application('application') + self.sections_list('sections')

        def get_acd(token):
            return Acd(token['application'], token['sections'])

        self.acd.setParseAction(get_acd)

    def parse_attribute(self, string):
        return self.attribute.parseString(string)[0]

    def parse_attributes_list(self, string):
        r = self.attributes_list.parseString(string)[0]
        attributes_list = [item for item in r]
        return attributes_list

    def parse_parameter(self, string):
        return self.parameter.parseString(string)[0]

    def parse_parameters_list(self, string):
        r = self.parameters_list.parseString(string)[0]
        parameters_list = [item for item in r]
        return parameters_list

    def parse_application(self, string):
        return self.application.parseString(string)[0]

    def parse_section(self, string):
        return self.section.parseString(string)[0]

    def parse_sections(self, string):
        r = self.sections_list.parseString(string)[0]
        sections_list = [item for item in r]
        return sections_list

    def parse_acd(self, string):
        return self.acd.parseString(string)[0]
