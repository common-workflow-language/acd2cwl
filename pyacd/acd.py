"""
The acd module defines an object model for ACD files contents
"""
# pylint: disable=too-few-public-methods, missing-docstring
import sys

SEQUENCE_FORMATS = {
    'abi': {'try': True,
            'Nuc': True,
            'Pro': True,
            'Feat': False,
            'Gap': True,
            'Mset': False,
            'description': 'ABI trace file',
            'input': True},
    'acedb': {'try': True,
              'Nuc': True,
              'Pro': True,
              'Feat': False,
              'Gap': True,
              'Mset': False,
              'description': 'ACEDB sequence format',
              'input': True,
              'output': True,
              'Sngl': False,
              'Save': False},
    'asn1': {'Nuc': True,
             'Pro': True,
             'Feat': False,
             'Gap': True,
             'Mset': False,
             'description': 'NCBI ASN.1 format',
             'input': True,
             'output': True,
             'Sngl': False,
             'Save': False},
    'clustal': {'try': True,
                'Nuc': True,
                'Pro': True,
                'Feat': False,
                'Gap': True,
                'Mset': False,
                'description': 'Clustalw output format',
                'input': True,
                'output': True,
                'Sngl': False,
                'Save': True},
    'codata': {'try': True,
               'Nuc': True,
               'Pro': True,
               'Feat': True,
               'Gap': True,
               'Mset': False,
               'description': 'CODATA entry format',
               'input': True,
               'output': True,
               'Sngl': False,
               'Save': False},
    'das': {'Nuc': True,
            'Pro': True,
            'Feat': False,
            'Gap': True,
            'Mset': False,
            'description': 'DASSEQUENCE DAS any sequence',
            'input': False,
            'output': True,
            'Sngl': False,
            'Save': False},
    'dasdna': {'Nuc': True,
               'Pro': False,
               'Feat': False,
               'Gap': True,
               'Mset': False,
               'description': 'DASDNA DAS nucleotide-only sequence',
               'input': False,
               'output': True,
               'Sngl': False,
               'Save': False},
    'dbid': {'try': False,
             'Nuc': True,
             'Pro': True,
             'Feat': False,
             'Gap': True,
             'Mset': False,
             'description':
             'FASTA format variant with database name before ID'},
    'embl': {'try': True,
             'Nuc': True,
             'Pro': False,
             'Feat': True,
             'Gap': True,
             'Mset': False,
             'description': 'EMBL entry format'},
    'experiment': {'try': True,
                   'Nuc': True,
                   'Pro': True,
                   'Feat': False,
                   'Gap': True,
                   'Mset': False,
                   'description': 'Staden experiment file'},
    'fasta': {'try': True,
              'Nuc': True,
              'Pro': True,
              'Feat': False,
              'Gap': True,
              'Mset': False,
              'description': 'FASTA format including NCBI-style IDs'},
    'fastq': {'try': True,
              'Nuc': True,
              'Pro': False,
              'Feat': False,
              'Gap': False,
              'Mset': False,
              'description':
              'Fastq short read format ignoring quality scores'},
    'fastq-illumina': {'try': False,
                       'Nuc': True,
                       'Pro': False,
                       'Feat': False,
                       'Gap': False,
                       'Mset': False,
                       'description': 'Fastq Illumina 1.3 short read format'},
    'fastq-sanger': {'try': False,
                     'Nuc': True,
                     'Pro': False,
                     'Feat': False,
                     'Gap': False,
                     'Mset': False,
                     'description':
                     'Fastq short read format with Phred quality'},
    'fastq-solexa': {'try': False,
                     'Nuc': True,
                     'Pro': False,
                     'Feat': False,
                     'Gap': False,
                     'Mset': False,
                     'description':
                     'Fastq Solexa/Illumina 1.0 short read format'},
    'fitch': {'try': True,
              'Nuc': True,
              'Pro': True,
              'Feat': False,
              'Gap': True,
              'Mset': False,
              'description': 'Fitch program format'},
    'gcg': {'try': True,
            'Nuc': True,
            'Pro': True,
            'Feat': False,
            'Gap': True,
            'Mset': False,
            'description': 'GCG sequence format'},
    'genbank': {'try': True,
                'Nuc': True,
                'Pro': False,
                'Feat': True,
                'Gap': True,
                'Mset': False,
                'description': 'Genbank entry format'},
    'genpept': {'try': False,
                'Nuc': False,
                'Pro': True,
                'Feat': True,
                'Gap': True,
                'Mset': False,
                'description': 'Refseq protein entry format (alias)'},
    'gff2': {'try': True,
             'Nuc': True,
             'Pro': True,
             'Feat': True,
             'Gap': True,
             'Mset': False,
             'description': 'GFF feature file with sequence in the header'},
    'gff3': {'try': True,
             'Nuc': True,
             'Pro': True,
             'Feat': True,
             'Gap': True,
             'Mset': False,
             'description': 'GFF3 feature file with sequence'},
    'gifasta': {'try': False,
                'Nuc': True,
                'Pro': True,
                'Feat': False,
                'Gap': True,
                'Mset': False,
                'description':
                'FASTA format including NCBI-style GIs (alias)'},
    'hennig86': {'try': True,
                 'Nuc': True,
                 'Pro': True,
                 'Feat': False,
                 'Gap': True,
                 'Mset': False,
                 'description': 'Hennig86 output format'},
    'ig': {'try': False,
           'Nuc': True,
           'Pro': True,
           'Feat': False,
           'Gap': True,
           'Mset': False,
           'description': 'Intelligenetics sequence format'},
    'igstrict': {'try': True,
                 'Nuc': True,
                 'Pro': True,
                 'Feat': False,
                 'Gap': True,
                 'Mset': False,
                 'description':
                 'Intelligenetics sequence format strict parser'},
    'jackkniffer': {'try': True,
                    'Nuc': True,
                    'Pro': True,
                    'Feat': False,
                    'Gap': True,
                    'Mset': False,
                    'description':
                    'Jackknifer interleaved and non-interleaved formats'},
    'mase': {'try': False,
             'Nuc': True,
             'Pro': True,
             'Feat': False,
             'Gap': True,
             'Mset': False,
             'description': 'MASE program format'},
    'mega': {'try': True,
             'Nuc': True,
             'Pro': True,
             'Feat': False,
             'Gap': True,
             'Mset': False,
             'description': 'MEGA interleaved and non-interleaved formats'},
    'msf': {'try': True,
            'Nuc': True,
            'Pro': True,
            'Feat': False,
            'Gap': True,
            'Mset': False,
            'description': 'GCG MSF (multiple sequence file) file format'},
    'nbrf': {'try': True,
             'Nuc': True,
             'Pro': True,
             'Feat': True,
             'Gap': True,
             'Mset': False,
             'description': 'NBRF/PIR entry format'},
    'nexus': {'try': True,
              'Nuc': True,
              'Pro': True,
              'Feat': False,
              'Gap': True,
              'Mset': False,
              'description': 'NEXUS/PAUP interleaved format'},
    'pdb': {'try': True,
            'Nuc': False,
            'Pro': True,
            'Feat': False,
            'Gap': False,
            'Mset': False,
            'description': 'PDB protein databank format ATOM lines'},
    'pdbnuc': {'try': False,
               'Nuc': True,
               'Pro': False,
               'Feat': False,
               'Gap': False,
               'Mset': False,
               'description':
               'PDB protein databank format nucleotide ATOM lines'},
    'pdbnucseq': {'try': False,
                  'Nuc': True,
                  'Pro': False,
                  'Feat': False,
                  'Gap': False,
                  'Mset': False,
                  'description':
                  'PDB protein databank format nucleotide SEQRES lines'},
    'pdbseq': {'try': True,
               'Nuc': False,
               'Pro': True,
               'Feat': False,
               'Gap': False,
               'Mset': False,
               'description': 'PDB protein databank format SEQRES lines'},
    'pearson': {'try': True,
                'Nuc': True,
                'Pro': True,
                'Feat': False,
                'Gap': True,
                'Mset': False,
                'description':
                'Plain old FASTA format with IDs not parsed further'},
    'phylip': {'try': True,
               'Nuc': True,
               'Pro': True,
               'Feat': False,
               'Gap': True,
               'Mset': True,
               'description':
               'PHYLIP interleaved and non-interleaved formats'},
    'phylipnon': {'try': False,
                  'Nuc': True,
                  'Pro': True,
                  'Feat': False,
                  'Gap': True,
                  'Mset': True,
                  'description': 'PHYLIP non-interleaved format'},
    'raw': {'try': True,
            'Nuc': True,
            'Pro': True,
            'Feat': False,
            'Gap': False,
            'Mset': False,
            'description': 'Raw sequence with no non-sequence characters'},
    'refseqp': {'try': False,
                'Nuc': False,
                'Pro': True,
                'Feat': True,
                'Gap': True,
                'Mset': False,
                'description': 'RefseqP entry format'},
    'selex': {'try': False,
              'Nuc': True,
              'Pro': True,
              'Feat': False,
              'Gap': True,
              'Mset': False,
              'description': 'SELEX format'},
    'staden': {'try': False,
               'Nuc': True,
               'Pro': True,
               'Feat': False,
               'Gap': True,
               'Mset': True,
               'description': 'Old Staden package sequence format'},
    'stockholm': {'try': True,
                  'Nuc': True,
                  'Pro': True,
                  'Feat': False,
                  'Gap': True,
                  'Mset': False,
                  'description': 'Stockholm (pfam) format'},
    'strider': {'try': True,
                'Nuc': True,
                'Pro': True,
                'Feat': False,
                'Gap': True,
                'Mset': False,
                'description': 'DNA Strider output format'},
    'swiss': {'try': True,
              'Nuc': False,
              'Pro': True,
              'Feat': True,
              'Gap': True,
              'Mset': False,
              'description': 'SwissProt entry format'},
    'text': {'try': False,
             'Nuc': True,
             'Pro': True,
             'Feat': False,
             'Gap': True,
             'Mset': False,
             'description': 'Plain text'},
    'treecon': {'try': True,
                'Nuc': True,
                'Pro': True,
                'Feat': False,
                'Gap': True,
                'Mset': False,
                'description': 'Treecon output format'},
}


class Acd(object):
    """
    ACD description
    """
    def __init__(self, application=None, sections=None):
        self.application = application
        self.sections = sections or []


class UnknownAcdPropertyException(Exception):
    """
    Exception thrown when trying to set a value to an unknown property
    """
    def __init__(self, attribute_name, attribute_value, parameter_name):
        super(UnknownAcdPropertyException, self).__init__()
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.parameter_name = parameter_name

    def __str__(self):
        template = 'trying to set unknown property "{0}" to "{1}" in ' +\
                   'parameter "{2}"'
        return template.format(self.attribute_name, self.attribute_value,
                               self.parameter_name)


class InvalidAcdPropertyValue(Exception):
    """
    Exception thrown when trying to set an invalid value to an ACD property
    """
    def __init__(self, attribute_name, attribute_value, parameter_name):
        super(InvalidAcdPropertyValue, self).__init__()
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value
        self.parameter_name = parameter_name

    def __str__(self):
        template = 'trying to set value of property "{0}" to invalid value ' +\
                   '"{1}" in parameter "{2}"'
        return template.format(self.attribute_name, self.attribute_value,
                               self.parameter_name)


class ElementWithAttributes(object):
    """
    Abstract class to structure an ACD element that has some attributes
    """
    def set_attributes(self, attributes):
        """
        Set the values for the attributes of the element, based on
        the existing default values
        :param attributes: the attributes to be set
        :type attributes: dict
        :return:
        """
        # pylint: disable=no-member
        for attribute in attributes:
            if attribute.name in self.attributes:
                if attribute.value.startswith(
                        '$') or attribute.value.startswith('@'):
                    # computed attribute values
                    self.attributes[attribute.name] = attribute.value
                try:
                    if isinstance(self.attributes[attribute.name], list):
                        self.attributes[attribute.name].append(attribute.value)
                    elif isinstance(self.attributes[attribute.name], bool):
                        if attribute.value in ['yes', 'Y', 'y', 'true']:
                            self.attributes[attribute.name] = True
                        elif attribute.value in ['no', 'N', 'n', 'false']:
                            self.attributes[attribute.name] = False
                        else:
                            raise InvalidAcdPropertyValue(
                                attribute.name, attribute.value, self.name)
                    else:
                        self.attributes[attribute.name] = type(self.attributes[
                            attribute.name])(attribute.value)
                except TypeError as terr:
                    print "Error while trying to set value of {0} to {1} in " \
                          "parameter {2}" \
                          "".format(attribute.name, attribute.value, self.name)
                    raise terr
            elif attribute.name in self.qualifiers:
                if attribute.value.startswith(
                        '$') or attribute.value.startswith('@'):
                    # computed qualifier values
                    self.qualifiers[attribute.name] = attribute.value
                try:
                    if isinstance(self.qualifiers[attribute.name], list):
                        self.qualifiers[attribute.name].append(attribute.value)
                    elif isinstance(self.qualifiers[attribute.name], bool):
                        if attribute.value in ['yes', 'Y', 'y', 'true']:
                            self.qualifiers[attribute.name] = True
                        elif attribute.value in ['no', 'N', 'n', 'false']:
                            self.qualifiers[attribute.name] = False
                        else:
                            raise InvalidAcdPropertyValue(
                                attribute.name, attribute.value, self.name)
                    else:
                        self.qualifiers[attribute.name] = type(self.qualifiers[
                            attribute.name])(attribute.value)
                except TypeError as terr:
                    print "Error while trying to set value of {0} to " \
                               "{1} in parameter {2}".format(attribute.name,
                                                             attribute.value,
                                                             self.name)
                    raise terr
            else:
                raise UnknownAcdPropertyException(attribute.name,
                                                  attribute.value, self.name)


class Application(ElementWithAttributes):
    """
    ACD Application block
    """
    def __init__(self, name, attributes=None):
        """
        :param name: name of the application
        :type name: basestring
        :param attributes: attributes of the Application block
        :type attributes: dict
        """
        self.name = name
        self.attributes = {'documentation': '',
                           'relations': [],
                           'groups': '',
                           'keywords': [],
                           'gui': True,
                           'batch': True,
                           'embassy': '',
                           'external': '',
                           'cpu': '',
                           'supplier': '',
                           'version': '',
                           'nonemboss': '',
                           'executable': '',
                           'template': '',
                           'comment': '',
                           'obsolete': ''}
        if attributes is not None:
            self.set_attributes(attributes)


class Section(ElementWithAttributes):
    """
    ACD parameters section block
    """
    def __init__(self, name, properties=None, parameters=None):
        """
        :param name: name of the section
        :type name: basestring
        :param properties: the properties to set
        :type properties: list
        :param parameters: the parameters of the section
        :type parameters: list
        """
        self.name = name
        self.properties = properties or []
        self.parameters = parameters or []


INPUT = 'input parameter type'
""" input parameter type """

OUTPUT = 'output parameter type'
""" output parameter type """


class Parameter(ElementWithAttributes):
    """
    ACD Parameter block
    """
    type = INPUT
    """ type of the parameter, input or output """

    def __init__(self, name, datatype, attributes):
        """
        :param name: name of the parameter
        :type name: basestring
        :param datatype: the datatype of the parameter (one of the keys of
        PARAMETER_CLASSES
        :type datatype: dict
        :param attributes: attribute values for the parameter
        :type attributes: dict
        """
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
                           'default': '', }
        self.qualifiers = {}


PARAMETER_CLASSES = {}


class ArrayParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ArrayParameter, self)._init_attribute_defaults()
        self.description = 'List of floating point numbers'
        self.attributes.update({'size': 1,
                                'minimum': -sys.float_info.max,
                                'maximum': sys.float_info.max,
                                'sum': 1.0,
                                'sumtest': True,
                                'warnrange': True,
                                'increment': 0,
                                'precision': 3,
                                'trueminimum': False,
                                'failrange': False,
                                'rangemessage': '',
                                'tolerance': 0.01})


PARAMETER_CLASSES['array'] = ArrayParameter


class BooleanParameter(Parameter):
    def _init_attribute_defaults(self):
        super(BooleanParameter, self)._init_attribute_defaults()
        self.description = 'Boolean value Yes/No'
        self.attributes.update({'default': False})


PARAMETER_CLASSES['boolean'] = BooleanParameter


class FloatParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FloatParameter, self)._init_attribute_defaults()
        self.description = 'Floating point number'
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


PARAMETER_CLASSES['float'] = FloatParameter


class IntegerParameter(Parameter):
    def _init_attribute_defaults(self):
        super(IntegerParameter, self)._init_attribute_defaults()
        self.description = 'Integer'
        self.attributes.update({'minimum': -sys.maxint,
                                'maximum': sys.maxint,
                                'default': 0,
                                'increment': 0,
                                'trueminimum': False,
                                'warnrange': True,
                                'failrange': False,
                                'rangemessage': '',
                                'large': False})


PARAMETER_CLASSES['integer'] = IntegerParameter


class RangeParameter(Parameter):
    def _init_attribute_defaults(self):
        super(RangeParameter, self)._init_attribute_defaults()
        self.description = 'Sequence range'
        self.attributes.update({'minimum': 1,
                                'maximum': sys.maxint,
                                'trueminimum': False,
                                'warnrange': True,
                                'failrange': False,
                                'rangemessage': '',
                                'size': 0,
                                'minsize': 0})


PARAMETER_CLASSES['range'] = RangeParameter


class StringParameter(Parameter):
    def _init_attribute_defaults(self):
        super(StringParameter, self)._init_attribute_defaults()
        self.description = 'String value'
        self.attributes.update({'minlength': 0,
                                'maxlength': sys.maxint,
                                'pattern': '',
                                'upper': False,
                                'lower': False,
                                'word': False})


PARAMETER_CLASSES['string'] = StringParameter


class ToggleParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ToggleParameter, self)._init_attribute_defaults()
        self.description = 'Toggle value Yes/No'


PARAMETER_CLASSES['toggle'] = ToggleParameter


class AssemblyParameter(Parameter):
    def _init_attribute_defaults(self):
        super(AssemblyParameter, self)._init_attribute_defaults()
        self.description = 'Assembly of sequence reads'
        self.attributes.update({'entry': False, 'nullok': False})
        self.qualifiers.update({'cbegin': 0,
                                'cend': 0,
                                'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})


PARAMETER_CLASSES['assembly'] = AssemblyParameter


class CodonParameter(Parameter):
    def _init_attribute_defaults(self):
        super(CodonParameter, self)._init_attribute_defaults()
        self.description = 'Codon usage file in EMBOSS data path'
        self.attributes.update({'name': 'Ehum.cut',
                                'nullok': False})
        self.qualifiers.update({'format': ''})

PARAMETER_CLASSES['codon'] = CodonParameter


class CPDBParameter(Parameter):
    def _init_attribute_defaults(self):
        super(CPDBParameter, self)._init_attribute_defaults()
        self.description = 'Clean PDB file'
        self.attributes.update({'nullok': False})
        self.qualifiers.update({'format': ''})

PARAMETER_CLASSES['cpdb'] = CPDBParameter


class DataFileParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DataFileParameter, self)._init_attribute_defaults()
        self.description = 'Data file'
        self.attributes.update({'name': '',
                                'extension': '',
                                'directory': '',
                                'nullok': False})

PARAMETER_CLASSES['datafile'] = DataFileParameter


class DirectoryParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DirectoryParameter, self)._init_attribute_defaults()
        self.description = 'Directory'
        self.attributes.update({'fullpath': False,
                                'nulldefault': False,
                                'nullok': False})
        self.qualifiers.update({'extension': ''})

PARAMETER_CLASSES['directory'] = DirectoryParameter


class DirListParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DirListParameter, self)._init_attribute_defaults()
        self.description = 'Directory with files'
        self.attributes.update({'fullpath': False,
                                'nullok': False})
        self.qualifiers.update({'extension': ''})

PARAMETER_CLASSES['dirlist'] = DirListParameter


class DiscreteStatesParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DiscreteStatesParameter, self)._init_attribute_defaults()
        self.description = 'Discrete states file'
        self.attributes.update({'length': 0,
                                'size': 1,
                                'characters': '01',
                                'nullok': False})

PARAMETER_CLASSES['discretestates'] = DiscreteStatesParameter


class DistancesParameter(Parameter):
    def _init_attribute_defaults(self):
        super(DistancesParameter, self)._init_attribute_defaults()
        self.description = 'Distance matrix'
        self.attributes.update({'missval': False, 'size': 1, 'nullok': False})

PARAMETER_CLASSES['distances'] = DistancesParameter


class FeaturesParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FeaturesParameter, self)._init_attribute_defaults()
        self.description = 'Readable feature table'
        self.attributes.update({'type': '',
                                'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'fformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'fopenfile': '',
                                'fask': False,
                                'fbegin': 0,
                                'fend': 0,
                                'freverse': False,
                                'fcircular': False})

PARAMETER_CLASSES['features'] = FeaturesParameter


class FileListParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FileListParameter, self)._init_attribute_defaults()
        self.description = 'Comma-separated file list'
        self.attributes.update({'binary': False, 'nullok': False})

PARAMETER_CLASSES['filelist'] = FileListParameter


class FrequenciesParameter(Parameter):
    def _init_attribute_defaults(self):
        super(FrequenciesParameter, self)._init_attribute_defaults()
        self.description = 'Frequency value(s)'
        self.attributes.update({'length': 0,
                                'size': 1,
                                'continuous': False,
                                'genedata': False,
                                'within': False,
                                'nullok': False})

PARAMETER_CLASSES['frequencies'] = FrequenciesParameter


class InFileParameter(Parameter):
    '''Input file'''

    def _init_attribute_defaults(self):
        super(InFileParameter, self)._init_attribute_defaults()
        self.description = 'Input file'
        self.attributes.update({'directory': '',
                                'trydefault': False,
                                'binary': False,
                                'nullok': False})

PARAMETER_CLASSES['infile'] = InFileParameter


class MatrixParameter(Parameter):
    '''Input file'''

    def _init_attribute_defaults(self):
        super(MatrixParameter, self)._init_attribute_defaults()
        self.description = 'Comparison matrix file in EMBOSS data path'
        self.attributes.update({'protein': True,
                                'pname': 'EBLOSUM62',
                                'nname': 'EDNAFULL'})

PARAMETER_CLASSES['matrix'] = MatrixParameter
PARAMETER_CLASSES['matrixf'] = MatrixParameter


class OBOParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OBOParameter, self)._init_attribute_defaults()
        self.description = 'OBO bio-ontology term(s)'
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})

PARAMETER_CLASSES['obo'] = OBOParameter


class PatternParameter(Parameter):
    def _init_attribute_defaults(self):
        super(PatternParameter, self)._init_attribute_defaults()
        self.description = 'Sequence pattern'
        self.attributes.update({'minlength': 1,
                                'maxlength': sys.maxint,
                                'maxsize': sys.maxint,
                                'upper': False,
                                'lower': False,
                                'type': 'string'})
        self.qualifiers.update({'pformat': '',
                                'pmismatch': 0,
                                'pname': ''})

PARAMETER_CLASSES['pattern'] = PatternParameter


class PropertiesParameter(Parameter):
    def _init_attribute_defaults(self):
        super(PropertiesParameter, self)._init_attribute_defaults()
        self.description = 'Property value(s)'
        self.attributes.update({'length': 0,
                                'size': '1',
                                'characters': '',
                                'nullok': False})

PARAMETER_CLASSES['properties'] = PropertiesParameter


class RefseqParameter(Parameter):
    def _init_attribute_defaults(self):
        super(RefseqParameter, self)._init_attribute_defaults()
        self.description = 'Reference sequence'
        self.attributes.update({'entry': False, 'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})

PARAMETER_CLASSES['refseq'] = RefseqParameter


class RegexpParameter(Parameter):
    def _init_attribute_defaults(self):
        super(RegexpParameter, self)._init_attribute_defaults()
        self.description = 'Regular expression pattern'
        self.attributes.update({'minlength': 1,
                                'maxlength': sys.maxint,
                                'maxsize': sys.maxint,
                                'upper': False,
                                'lower': False,
                                'type': 'string'})
        self.qualifiers.update({'pformat': '', 'pname': ''})

PARAMETER_CLASSES['regexp'] = RegexpParameter


class ResourceParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ResourceParameter, self)._init_attribute_defaults()
        self.description = 'Data resource catalogue entry(s)'
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})

PARAMETER_CLASSES['resource'] = ResourceParameter


class ScopParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ScopParameter, self)._init_attribute_defaults()
        self.description = 'SCOP and CATH domain classification data in DCF'
        self.attributes.update({'nullok': False})
        self.qualifiers.update({'format': ''})

PARAMETER_CLASSES['scop'] = ScopParameter


class ListParameter(Parameter):
    def _init_attribute_defaults(self):
        super(ListParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': 1,
                                'maximum': 1,
                                'button': False,
                                'casesensitive': False,
                                'header': '',
                                'delimiter': ";",
                                'codedelimiter': ':',
                                'values': ''})

PARAMETER_CLASSES['list'] = ListParameter


class SelectionParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SelectionParameter, self)._init_attribute_defaults()
        self.attributes.update({'minimum': 1,
                                'maximum': 1,
                                'button': False,
                                'casesensitive': False,
                                'header': '',
                                'delimiter': ";",
                                'values': ''})

PARAMETER_CLASSES['selection'] = SelectionParameter


class SequenceParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SequenceParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'features': False,
                                'entry': False,
                                'nullok': False})
        self.qualifiers.update({'sbegin': 0,
                                'send': 0,
                                'sreverse': False,
                                'sask': False,
                                'snucleotide': False,
                                'sprotein': False,
                                'slower': False,
                                'supper': False,
                                'scircular': False,
                                'squick': False,
                                'sformat': '',
                                'iquery': '',
                                'ioffset': 0,
                                'sdbname': '',
                                'sid': '',
                                'ufo': '',
                                'fformat': '',
                                'fopenfile': ''})

PARAMETER_CLASSES['sequence'] = SequenceParameter


class SeqAllParameter(Parameter):
    def _init_attribute_defaults(self):
        super(SeqAllParameter, self)._init_attribute_defaults()
        self.attributes.update({'type': '',
                                'features': False,
                                'entry': False,
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'sbegin': 0,
                                'send': 0,
                                'sreverse': False,
                                'sask': False,
                                'snucleotide': False,
                                'sprotein': False,
                                'slower': False,
                                'supper': False,
                                'scircular': False,
                                'squick': False,
                                'sformat': '',
                                'iquery': '',
                                'ioffset': 0,
                                'sdbname': '',
                                'sid': '',
                                'ufo': '',
                                'fformat': '',
                                'fopenfile': ''})

PARAMETER_CLASSES['seqall'] = SeqAllParameter


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
        self.qualifiers.update({'sbegin': 0,
                                'send': 0,
                                'sreverse': False,
                                'sask': False,
                                'snucleotide': False,
                                'sprotein': False,
                                'slower': False,
                                'supper': False,
                                'scircular': False,
                                'squick': False,
                                'sformat': '',
                                'iquery': '',
                                'ioffset': 0,
                                'sdbname': '',
                                'sid': '',
                                'ufo': '',
                                'fformat': '',
                                'fopenfile': ''})

PARAMETER_CLASSES['seqset'] = SeqSetParameter


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
        self.qualifiers.update({'sbegin': 0,
                                'send': 0,
                                'sreverse': False,
                                'sask': False,
                                'snucleotide': False,
                                'sprotein': False,
                                'slower': False,
                                'supper': False,
                                'scircular': False,
                                'squick': False,
                                'sformat': '',
                                'iquery': '',
                                'ioffset': 0,
                                'sdbname': '',
                                'sid': '',
                                'ufo': '',
                                'fformat': '',
                                'fopenfile': ''})

PARAMETER_CLASSES['seqsetall'] = SeqSetAllParameter


class AlignParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(AlignParameter, self)._init_attribute_defaults()
        self.description = 'Alignment output file'
        self.attributes.update({'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'multiple': False,
                                'type': '',
                                'taglist': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'aformat': '',
                                'aextension': '',
                                'adirectory': '',
                                'aname': '',
                                'awidth': 0,
                                'aaccshow': False,
                                'adescshow': False,
                                'ausashow': False,
                                'aglobal': False})

PARAMETER_CLASSES['align'] = AlignParameter


class FeatOutParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(FeatOutParameter, self)._init_attribute_defaults()
        self.description = 'Writeable feature table'
        self.attributes.update({'name': '',
                                'extension': '',
                                'type': '',
                                'multiple': False,
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'offormat': '',
                                'ofopenfile': '',
                                'ofextension': '',
                                'ofdirectory': '',
                                'ofname': '',
                                'ofsingle': False})


PARAMETER_CLASSES['featout'] = FeatOutParameter


class OutAssemblyParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutAssemblyParameter, self)._init_attribute_defaults()
        self.description = 'Assembly of sequence reads'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outassembly'] = OutAssemblyParameter


class OutCodonParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutCodonParameter, self)._init_attribute_defaults()
        self.description = 'Codon usage file'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outcodon'] = OutCodonParameter


class OutCpdbParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutCpdbParameter, self)._init_attribute_defaults()
        self.description = 'Cleaned PDB file'
        self.attributes.update({'extension': '',
                                'nullok': False,
                                'nulldefault': False})


PARAMETER_CLASSES['outcpdb'] = OutCpdbParameter


class OutDataParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutDataParameter, self)._init_attribute_defaults()
        self.description = 'Formatted output file'
        self.attributes.update({'type': '',
                                'nullok': False,
                                'nulldefault': False,
                                'binary': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outdata'] = OutDataParameter


class OutDirParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutDirParameter, self)._init_attribute_defaults()
        self.description = 'Output directory'
        self.attributes.update({'fullpath': False,
                                'nulldefault': False,
                                'nullok': False,
                                'binary': False,
                                'create': False,
                                'temporary': False})
        self.qualifiers.update({'extension': ''})


PARAMETER_CLASSES['outdir'] = OutDirParameter


class OutDiscreteParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutDiscreteParameter, self)._init_attribute_defaults()
        self.description = 'Discrete states file'
        self.attributes.update({'nulldefault': False, 'nullok': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outdiscrete'] = OutDiscreteParameter


class OutDistanceParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutDistanceParameter, self)._init_attribute_defaults()
        self.description = 'Distance matrix'
        self.attributes.update({'nulldefault': False, 'nullok': False})


PARAMETER_CLASSES['outdistance'] = OutDistanceParameter


class OutFileParameter(Parameter):
    def _init_attribute_defaults(self):
        super(OutFileParameter, self)._init_attribute_defaults()
        self.description = 'Output file'
        self.attributes.update({'name': '',
                                'extension': '',
                                'append': False,
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': ''})


PARAMETER_CLASSES['outfile'] = OutFileParameter


class OutFreqParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutFreqParameter, self)._init_attribute_defaults()
        self.description = 'Frequency value(s)'
        self.attributes.update({'nullok': False, 'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outfreq'] = OutFreqParameter


class OutMatrix(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutMatrix, self)._init_attribute_defaults()
        self.description = 'Comparison matrix file'
        self.attributes.update({'nullok': False, 'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outmatrix'] = OutMatrix


class OutMatrixF(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutMatrixF, self)._init_attribute_defaults()
        self.description = 'Comparison matrix file'
        self.attributes.update({'nullok': False, 'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outmatrixf'] = OutMatrixF


class OutOBO(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutOBO, self)._init_attribute_defaults()
        self.description = 'OBO ontology term(s)'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outobo'] = OutOBO


class OutProperties(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutProperties, self)._init_attribute_defaults()
        self.description = 'Property value(s)'
        self.attributes.update({'nullok': False, 'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outproperties'] = OutProperties


class OutRefseq(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutRefseq, self)._init_attribute_defaults()
        self.description = 'Reference sequence'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outrefseq'] = OutRefseq


class OutResource(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutResource, self)._init_attribute_defaults()
        self.description = 'Reference sequence'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outresource'] = OutResource


class OutScop(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutScop, self)._init_attribute_defaults()
        self.description = 'Property value(s)'
        self.attributes.update({'nullok': False, 'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outscop'] = OutScop


class OutTaxon(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutTaxon, self)._init_attribute_defaults()
        self.description = 'NCBI Taxonomy entries'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outtaxon'] = OutTaxon


class OutText(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutText, self)._init_attribute_defaults()
        self.description = 'Text entries'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outtext'] = OutText


class OutTree(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutTree, self)._init_attribute_defaults()
        self.description = 'Phylogenetic tree'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outtree'] = OutTree


class OutURL(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutURL, self)._init_attribute_defaults()
        self.description = 'URL entries'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outurl'] = OutURL


class OutVariation(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutVariation, self)._init_attribute_defaults()
        self.description = 'Variation entries'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outvariation'] = OutVariation


class OutXML(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(OutXML, self)._init_attribute_defaults()
        self.description = 'XML'
        self.attributes.update({'name': '',
                                'extension': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'odirectory': '', 'oformat': ''})


PARAMETER_CLASSES['outxml'] = OutXML


class ReportParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(ReportParameter, self)._init_attribute_defaults()
        self.description = 'Report output file'
        self.attributes.update({'multiple': False,
                                'precision': 3,
                                'type': '',
                                'taglist': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'rformat': '',
                                'rname': '',
                                'rextension': '',
                                'rdirectory': '',
                                'raccshow': False,
                                'rdesshow': False,
                                'rscoreshow': True,
                                'rstransshow': True,
                                'rusashow': False,
                                'rmaxall': 0,
                                'rmaxseq': 0})


PARAMETER_CLASSES['report'] = ReportParameter


class SeqOutParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(SeqOutParameter, self)._init_attribute_defaults()
        self.description = 'Writeable sequence'
        self.attributes.update({'name': '',
                                'extension': '',
                                'features': False,
                                'type': '',
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'osformat': '',
                                'osextension': '',
                                'osname': '',
                                'osdirectory': '',
                                'osdbname': '',
                                'ossingle': False,
                                'oufo': '',
                                'offormat': '',
                                'ofname': '',
                                'ofdirectory': ''})


PARAMETER_CLASSES['seqout'] = SeqOutParameter


class SeqOutAllParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(SeqOutAllParameter, self)._init_attribute_defaults()
        self.description = 'Writeable sequence(s)'
        self.attributes.update({'name': '',
                                'extension': '',
                                'features': False,
                                'type': '',
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'aligned': False,
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'osformat': 'fasta',
                                'osextension': '',
                                'osname': '',
                                'osdirectory': '',
                                'osdbname': '',
                                'ossingle': False,
                                'oufo': '',
                                'offormat': '',
                                'ofname': '',
                                'ofdirectory': ''})


PARAMETER_CLASSES['seqoutall'] = SeqOutAllParameter


class SeqOutSetParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(SeqOutSetParameter, self)._init_attribute_defaults()
        self.description = 'Writeable sequences'
        self.attributes.update({'name': '',
                                'extension': '',
                                'features': False,
                                'type': '',
                                'minseqs': 1,
                                'maxseqs': sys.maxint,
                                'aligned': False,
                                'nullok': False,
                                'nulldefault': False})
        self.qualifiers.update({'osformat': '',
                                'osextension': '',
                                'osname': '',
                                'osdirectory': '',
                                'osdbname': '',
                                'ossingle': False,
                                'oufo': '',
                                'offormat': '',
                                'ofname': '',
                                'ofdirectory': ''})


PARAMETER_CLASSES['seqoutset'] = SeqOutSetParameter


class GraphParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(GraphParameter, self)._init_attribute_defaults()
        self.description = 'Graph device for a general graph'
        self.attributes.update({'sequence': False,
                                'nullok': False,
                                'nulldefault': False,
                                'gprompt': False,
                                'gdesc': '',
                                'gtitle': '',
                                'gsubtitle': '',
                                'gxtitle': '',
                                'gytitle': '',
                                'goutfile': '',
                                'gdirectory': ''})


PARAMETER_CLASSES['graph'] = GraphParameter


class XYGraphParameter(Parameter):

    type = OUTPUT

    def _init_attribute_defaults(self):
        super(XYGraphParameter, self)._init_attribute_defaults()
        self.description = 'Graph device for a 2D graph'
        self.attributes.update({'sequence': False,
                                'multiple': 1,
                                'nullok': False,
                                'nulldefault': False,
                                'gprompt': False,
                                'gdesc': '',
                                'gtitle': '',
                                'gsubtitle': '',
                                'gxtitle': '',
                                'gytitle': '',
                                'goutfile': '',
                                'gdirectory': ''})

PARAMETER_CLASSES['xygraph'] = XYGraphParameter


class TaxonParameter(Parameter):
    def _init_attribute_defaults(self):
        super(TaxonParameter, self)._init_attribute_defaults()
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})


PARAMETER_CLASSES['taxon'] = TaxonParameter


class TextParameter(Parameter):
    def _init_attribute_defaults(self):
        super(TextParameter, self)._init_attribute_defaults()
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})


PARAMETER_CLASSES['text'] = TextParameter


class TreeParameter(Parameter):
    def _init_attribute_defaults(self):
        super(TreeParameter, self)._init_attribute_defaults()
        self.attributes.update({'size': 0, 'nullok': False})


PARAMETER_CLASSES['tree'] = TreeParameter


class URLParameter(Parameter):
    def _init_attribute_defaults(self):
        super(URLParameter, self)._init_attribute_defaults()
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'idbname': '',
                                'swiss': False,
                                'embl': False,
                                'accession': '',
                                'identifier': ''})


PARAMETER_CLASSES['url'] = URLParameter


class VariationParameter(Parameter):
    def _init_attribute_defaults(self):
        super(VariationParameter, self)._init_attribute_defaults()
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})
        self.qualifiers.update({'iformat': '',
                                'iquery': '',
                                'ioffset': '',
                                'idbname': ''})


PARAMETER_CLASSES['variation'] = VariationParameter


class XMLParameter(Parameter):
    def _init_attribute_defaults(self):
        super(XMLParameter, self)._init_attribute_defaults()
        self.attributes.update({'entry': False,
                                'minreads': 1,
                                'maxreads': sys.maxint,
                                'nullok': False})


PARAMETER_CLASSES['xml'] = XMLParameter


def get_parameter(name, datatype, properties):
    """
    Build a Parameter object using its name, datatype and properties list
    :param name: name of the parameter
    :type name: basestring
    :param datatype: datatype of the parameter (must be a value of
    PARAMETER_CLASSES keys
    :type datatype: basestring
    :param properties: property values to be set in attributes or qualifiers
    :type properties: dict
    """
    return PARAMETER_CLASSES.get(datatype, Parameter)(name, datatype,
                                                      properties)


class Attribute(object):
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
