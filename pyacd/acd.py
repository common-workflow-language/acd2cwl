import sys

class Acd(object):
    def __init__(self, application=None, sections=[]):
        self.application = application
        self.sections = sections

class UnknownAcdPropertyException(Exception):

    def __init__(self, attribute_name, attribute_value, parameter_name, *args, **kwargs):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.parameter_name = parameter_name
        super(Exception, self).__init__('trying to set unknown property "{0}" to "{1}" in parameter "{2}"'.format(self.attribute_name, self.attribute_value, self.parameter_name))

class InvalidAcdPropertyValue(Exception):

    def __init__(self, attribute_name, attribute_value, parameter_name, *args, **kwargs):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.parameter_name = parameter_name
        super(Exception, self).__init__('trying to set value of property "{0}" to invalid value "{1}" in parameter "{2}"'.format(self.attribute_name, self.attribute_value, self.parameter_name))

class ElementWithAttributes(object):
    def set_attributes(self, attributes):
        for attribute in attributes:
            if self.attributes.has_key(attribute.name):
                if attribute.value.startswith('$') or attribute.value.startswith('@'):
                    #computed attribute values
                    self.attributes[attribute.name] = attribute.value
                try:
                    if type(self.attributes[attribute.name]) == list:
                        self.attributes[attribute.name].append(attribute.value)
                    elif type(self.attributes[attribute.name]) == bool:
                        if attribute.value in ['yes', 'Y', 'y', 'true']:
                            self.attributes[attribute.name] = True
                        elif attribute.value in ['no', 'N', 'n', 'false']:
                            self.attributes[attribute.name] = False
                        else:
                            raise InvalidAcdPropertyValue(attribute.name, attribute.value, self.name)
                    else:
                        self.attributes[attribute.name] = type(self.attributes[attribute.name])(attribute.value)
                except TypeError as terr:
                    print "Error while trying to set value of {0} to {1}".format(attribute.name, attribute.value,
                                                                                 self.name)
                    raise terr
            else:
                raise UnknownAcdPropertyException(attribute.name, attribute.value, self.name,
                    "trying to set unknown property {0} to {1} in parameter {2}".format(attribute.name, attribute.value,
                                                                                        self.name))


class Application(ElementWithAttributes):
    def __init__(self, name, attributes=[]):
        self.name = name
        self.attributes = {'documentation': '',
                           'relations': [],
                           'groups': '',
                           'keywords':[],
                           'gui': True,
                           'batch': True,
                           'embassy':'',
                           'external':'',
                           'cpu':'',
                           'supplier':'',
                           'version':'',
                           'nonemboss':'',
                           'executable':'',
                           'template':'',
                           'comment':''}
        self.set_attributes(attributes)


class Section(ElementWithAttributes):
    def __init__(self, name, properties=[], parameters=[]):
        self.name = name
        self.properties = properties
        self.parameters = parameters


class Parameter(ElementWithAttributes):

    def __init__(self, name, datatype, attributes):
        self._init_attribute_defaults()
        self.name = name
        self.datatype = datatype
        self.set_attributes(attributes)

    def _init_attribute_defaults(self):
        self.attributes = {'information': '',
                           'prompt': '',
                           'code': '',
                           'help': '',
                           'parameter': False,
                           'standard': False,
                           'additional': False,
                           'missing': False,
                           'valid': '',
                           'expected': '',
                           'needed': True,
                           'knowntype': '',
                           'relations': [],
                           'outputmodifier': False,
                           'style': '',
                           'qualifier': '',
                           'template': '',
                           'comment': '',
                           'pformat': '',
                           'pname': '',
                           'type': '',
                           'features': '',
                           'default': '',
                           }


parameterClasses = {}


class ArrayParameter(Parameter):

    def _init_attribute_defaults(self):
        super(ArrayParameter, self)._init_attribute_defaults()
        self.attributes.update({'size': 1,
                                'minimum': -sys.float_info.max,
                                'maximum': sys.float_info.max,
                                'sum': 1.0,
                                'sumtest': True,
                                'tolerance': 0.01,
                                'warnrange': True,
                                'increment': 0,
                                'precision': 3})


parameterClasses['array'] = ArrayParameter


class BooleanParameter(Parameter):
    pass


parameterClasses['boolean'] = BooleanParameter


class FloatParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FloatParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': -sys.float_info.max,
                                'maximum': sys.float_info.max,
                                'increment': 1.0,
                                'precision': 3,
                                'warnrange': True})


parameterClasses['float'] = FloatParameter

class IntegerParameter(Parameter):
    def _init_attribute_defaults(self):
        super(IntegerParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': -sys.maxint,
                                'maximum': sys.maxint,
                                'increment': 0,
                                'warnrange': True})


parameterClasses['integer'] = IntegerParameter


class ListParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ListParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': 1,
                                'maximum': 1,
                                'button':False,
                                'casesensitive':False,
                                'header':'',
                                'delimiter':";",
                                'codedelimiter':':',
                                'values':''})


parameterClasses['list'] = ListParameter

class SelectionParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SelectionParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': 1,
                                'maximum': 1,
                                'button':False,
                                'casesensitive':False,
                                'header':'',
                                'delimiter':";",
                                'values':''})


parameterClasses['selection'] = SelectionParameter

class SequenceParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SequenceParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'features': False,
                                'entry': False,
                                'nullok': False})

parameterClasses['sequence'] = SequenceParameter

class SeqAllParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqAllParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'features': False,
                                'entry': False,
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'nullok': False})

parameterClasses['seqall'] = SeqAllParameter

class SeqSetParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqSetParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'features': False,
                                'entry': False,
                                'aligned': False,
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'nullok': False})

parameterClasses['seqset'] = SeqSetParameter

class SeqSetAllParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqSetAllParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'features': False,
                                'entry': False,
                                'aligned': False,
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'minsets': 1,
                                'maxsets': sys.maxint,
                                'nullok': False})

parameterClasses['seqsetall'] = SeqSetAllParameter

class MatrixParameter(Parameter):
    def _init_attribute_defaults(self):
        super(MatrixParameter, self)._init_attribute_defaults()
        self.attributes.update({'pname': 'EBLOSUM62',
                                'nname': 'EDNAFULL',
                                'protein': True})

parameterClasses['matrix'] = MatrixParameter

class MatrixFParameter(Parameter):
    def _init_attribute_defaults(self):
        super(MatrixFParameter, self)._init_attribute_defaults()
        self.attributes.update({'pname': 'EBLOSUM62',
                                'nname': 'EDNAFULL',
                                'protein': True})

parameterClasses['matrixf'] = MatrixFParameter

class SeqOutParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqOutParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'features': False,
                                'type':'',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['seqout'] = SeqOutParameter

class SeqOutAllParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqOutAllParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'features': False,
                                'type':'',
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['seqoutall'] = SeqOutAllParameter

class SeqOutSetParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqOutSetParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'features': False,
                                'type':'',
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'aligned': False,
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['seqoutset'] = SeqOutSetParameter

class ReportParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ReportParameter, self)._init_attribute_defaults()
        self.attributes.update({'multiple': False,
                                'precision': 3,
                                'type':'',
                                'taglist':'',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['report'] = ReportParameter

class OutFileParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OutFileParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'append':False,
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['outfile'] = OutFileParameter

class OutFileAllParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OutFileAllParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['outfileall'] = OutFileAllParameter

class AlignParameter(Parameter):
    def _init_attribute_defaults(self):
        super(AlignParameter, self)._init_attribute_defaults()
        self.attributes.update({'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'multiple': False,
                                'type': '',
                                'taglist': '',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['align'] = AlignParameter

class FeatOutParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FeatOutParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'type': '',
                                'multiple': False,
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['featout'] = FeatOutParameter

class OutCodonParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OutCodonParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['outcodon'] = OutCodonParameter

class OutCpdbParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OutCpdbParameter, self)._init_attribute_defaults()
        self.attributes.update({'extension': '',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['outcpdb'] = OutCpdbParameter

class OutDataParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OutDataParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'nullok':False,
                                'nulldefault':False})

parameterClasses['outdata'] = OutDataParameter


def getParameter(name, datatype, properties):
    return parameterClasses.get(datatype, Parameter)(name, datatype, properties)


class Attribute(object):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value