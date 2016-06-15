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
                #print "trying to set unknown property {0} to {1} in parameter {2}".format(attribute.name, attribute.value, self.name)
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
                                'precision': 3,
                                'trueminimum': False,
                                'failrange': False,
                                'rangemessage':'',
                                'tolerance':0.01})


parameterClasses['array'] = ArrayParameter

class BooleanParameter(Parameter):
    def _init_attribute_defaults(self):
        super(BooleanParameter, self)._init_attribute_defaults()
        self.attributes.update({'default': False})

parameterClasses['boolean'] = BooleanParameter


class FloatParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FloatParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': -sys.float_info.max,
                                'maximum': sys.float_info.max,
                                'increment': 1.0,
                                'default': 0.0,
                                'precision': 3,
                                'trueminimum': False,
                                'warnrange': True,
                                'failrange': False,
                                'rangemessage': '',
                                'large': False})

parameterClasses['float'] = FloatParameter


class IntegerParameter(Parameter):
    def _init_attribute_defaults(self):
        super(IntegerParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': -sys.maxint,
                                'maximum': sys.maxint,
                                'default': 0,
                                'increment': 0,
                                'trueminimum': False,
                                'warnrange': True,
                                'failrange': False,
                                'rangemessage': '',
                                'large': False})


parameterClasses['integer'] = IntegerParameter

class RangeParameter(Parameter):
    def _init_attribute_defaults(self):
        super(RangeParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': 1,
                                'maximum': sys.maxint,
                                'trueminimum': False,
                                'warnrange': True,
                                'failrange': False,
                                'rangemessage': '',
                                'size': 0,
                                'minsize': 0})

parameterClasses['range'] = RangeParameter


class StringParameter(Parameter):
    def _init_attribute_defaults(self):
        super(StringParameter, self)._init_attribute_defaults()
        self.attributes.update({'minlength': 0,
                                'maxlength': sys.maxint,
                                'pattern': '',
                                'upper': False,
                                'lower': False,
                                'word': False})

parameterClasses['string'] = StringParameter

class ToggleParameter(Parameter):
    pass

parameterClasses['toggle'] = ToggleParameter

class AssemblyParameter(Parameter):
    def _init_attribute_defaults(self):
        super(AssemblyParameter, self)._init_attribute_defaults()
        self.attributes.update({'cbegin': 0,
                                'cend': 0,
                                'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': '',
                                'entry': False,
                                'nullok': False})

parameterClasses['assembly'] = AssemblyParameter

class CodonParameter(Parameter):
    def _init_attribute_defaults(self):
        super(CodonParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': 'Ehum.cut',
                                'format': '',
                                'nullok': False})

parameterClasses['codon'] = CodonParameter

class CPDBParameter(Parameter):
    '''Clean PDB file'''
    def _init_attribute_defaults(self):
        super(CPDBParameter, self)._init_attribute_defaults()
        self.attributes.update({'format': '',
                                'nullok': False})

parameterClasses['cpdb'] = CPDBParameter

class DataFileParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DataFileParameter, self)._init_attribute_defaults()
        self.attributes.update({'name': '',
                                'extension': '',
                                'directory': '',
                                'nullok': False})

parameterClasses['datafile'] = DataFileParameter

class DirectoryParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DirectoryParameter, self)._init_attribute_defaults()
        self.attributes.update({'fullpath': False,
                                'nulldefault': False,
                                'extension': '',
                                'nullok': False})

parameterClasses['directory'] = DirectoryParameter

class DirListParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DirListParameter, self)._init_attribute_defaults()
        self.attributes.update({'fullpath': False,
                                'extension': '',
                                'nullok': False})

parameterClasses['dirlist'] = DirListParameter

class DiscreteStatesParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DiscreteStatesParameter, self)._init_attribute_defaults()
        self.attributes.update({'length': 0,
                                'size': 1,
                                'characters': '01',
                                'nullok':False})

parameterClasses['discretestates'] = DiscreteStatesParameter

class DistancesParameter(Parameter):
    '''Distance Matrix'''
    def _init_attribute_defaults(self):
        super(DistancesParameter, self)._init_attribute_defaults()
        self.attributes.update({'missval': False,
                                'size': 1,
                                'nullok':False})

parameterClasses['distances'] = DistancesParameter

class FeaturesParameter(Parameter):
    '''Readable feature table'''
    def _init_attribute_defaults(self):
        super(FeaturesParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False,
                                'fformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'fopenfile': '',
                                'fask': False,
                                'fbegin': 0,
                                'fend': 0,
                                'freverse': False,
                                'fcircular': False})

parameterClasses['features'] = FeaturesParameter

class FileListParameter(Parameter):
    '''Comma-separated file list'''
    def _init_attribute_defaults(self):
        super(FileListParameter, self)._init_attribute_defaults()
        self.attributes.update({'binary': False,
                                'nullok': False})

parameterClasses['filelist'] = FileListParameter

class FrequenciesParameter(Parameter):
    '''Frequency value(s)'''
    def _init_attribute_defaults(self):
        super(FrequenciesParameter, self)._init_attribute_defaults()
        self.attributes.update({'length': 0,
                                'size': 1,
                                'continuous': False,
                                'genedata': False,
                                'within': False,
                                'nullok': False})

parameterClasses['frequencies'] = FrequenciesParameter

class InFileParameter(Parameter):
    '''Input file'''
    def _init_attribute_defaults(self):
        super(InFileParameter, self)._init_attribute_defaults()
        self.attributes.update({'directory': '',
                                'trydefault': False,
                                'binary': False,
                                'nullok': False})

parameterClasses['infile'] = InFileParameter

class MatrixParameter(Parameter):
    '''Input file'''
    def _init_attribute_defaults(self):
        super(MatrixParameter, self)._init_attribute_defaults()
        self.attributes.update({'protein': True,
                                'pname': 'EBLOSUM62',
                                'nname': 'EDNAFULL'})

parameterClasses['matrix'] = MatrixParameter
parameterClasses['matrixf'] = MatrixParameter

class PropertiesParameter(Parameter):
    '''Input file'''
    def _init_attribute_defaults(self):
        super(PropertiesParameter, self)._init_attribute_defaults()
        self.attributes.update({'length': 0,
                                'size': '1',
                                'characters': '',
                                'nullok': False})

parameterClasses['properties'] = PropertiesParameter

class ScopParameter(Parameter):
    '''SCOP and CATH domain classification data in DCF'''
    def _init_attribute_defaults(self):
        super(ScopParameter, self)._init_attribute_defaults()
        self.attributes.update({'nullok': False,
                                'format': ''})

parameterClasses['scop'] = ScopParameter


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
        self.attributes.update({'osformat':'',
                                'osextension':'',
                                'osname':'',
                                'osdirectory':'',
                                'osdbname':'',
                                'ossingle':'',
                                'oufo':'',
                                'offormat':'',
                                'ofname':'',
                                'ofdirectory':''})

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
        self.attributes.update({'osformat': '',
                                'osextension': '',
                                'osname': '',
                                'osdirectory': '',
                                'osdbname': '',
                                'ossingle': '',
                                'oufo': '',
                                'offormat': '',
                                'ofname': '',
                                'ofdirectory': ''})

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
        self.attributes.update({'osformat': '',
                                'osextension': '',
                                'osname': '',
                                'osdirectory': '',
                                'osdbname': '',
                                'ossingle': '',
                                'oufo': '',
                                'offormat': '',
                                'ofname': '',
                                'ofdirectory': ''})

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

class GraphParameter(Parameter):
    def _init_attribute_defaults(self):
        super(GraphParameter, self)._init_attribute_defaults()
        self.attributes.update({'sequence':False,
                                'nullok':False,
                                'nulldefault':False,
                                'gprompt': False,
                                'gdesc':'',
                                'gtitle':'',
                                'gsubtitle':'',
                                'gxtitle':'',
                                'gytitle':'',
                                'goutfile':'',
                                'gdirectory':''})

parameterClasses['graph'] = GraphParameter

class XYGraphParameter(Parameter):
    def _init_attribute_defaults(self):
        super(XYGraphParameter, self)._init_attribute_defaults()
        self.attributes.update({'sequence':False,
                                'multiple':1,
                                'nullok':False,
                                'nulldefault':False,
                                'gprompt': False,
                                'gdesc':'',
                                'gtitle':'',
                                'gsubtitle':'',
                                'gxtitle':'',
                                'gytitle':'',
                                'goutfile':'',
                                'gdirectory':''})

parameterClasses['xygraph'] = XYGraphParameter

class PatternParameter(Parameter):
    def _init_attribute_defaults(self):
        super(PatternParameter, self)._init_attribute_defaults()
        self.attributes.update({'minlength':1,
                                'maxlength':sys.maxint,
                                'maxsize':sys.maxint,
                                'upper':False,
                                'lower': False,
                                'type':'string',
                                'pformat':'',
                                'pmismatch':0,
                                'pname':''})

parameterClasses['pattern'] = PatternParameter


def getParameter(name, datatype, properties):
    return parameterClasses.get(datatype, Parameter)(name, datatype, properties)


class Attribute(object):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value