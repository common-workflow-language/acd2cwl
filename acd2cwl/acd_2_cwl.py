"""
  module to transform an ACD object into a CWL description
  (as a python dictionary)
"""
import copy

from pyacd.acd import PARAMETER_CLASSES, SEQUENCE_FORMATS, INPUT

DATATYPES = {type_key: parameter_class.type for type_key, parameter_class
             in PARAMETER_CLASSES.iteritems()}

DATATYPES_CWL = {'array': {'type': 'array', 'item': 'int'},
                 'boolean': {'type': 'boolean'},
                 'integer': {'type': 'int'},
                 'float': {'type': 'float'},
                 'range': {'type': 'File'},
                 'regexp': {'type': 'File'},
                 'pattern': {'type': 'File'},
                 'string': {'type': 'string'},
                 'toggle': {'type': 'File'},
                 'codon': {'type': 'File'},
                 'cpdb': {'type': 'File'},
                 'datafile': {'type': 'File'},
                 'directory': {'type': 'File'},
                 'dirlist': {'type': 'File'},
                 'discretestates': {'type': 'File'},
                 'distances': {'type': 'File'},
                 'features': {'type': 'File'},
                 'filelist': {'type': 'File'},
                 'frequencies': {'type': 'File'},
                 'infile': {'type': 'File'},
                 'matrix': {'type': 'File'},
                 'matrixf': {'type': 'File'},
                 'obo': {'type': 'File'},
                 'properties': {'type': 'File'},
                 'scop': {'type': 'File'},
                 'sequence': {'type': 'File'},
                 'seqall': {'type': 'File'},
                 'seqset': {'type': 'File'},
                 'seqsetall': {'type': 'File'},
                 'tree': {'type': 'File'},
                 'list': {'type': 'File'},
                 'selection': {'type': 'File'},
                 'align': {'type': 'File'},
                 'featout': {'type': 'File'},
                 'outobo': {'type': 'File'},
                 'outresource': {'type': 'File'},
                 'xml': {'type': 'File'},
                 'outxml': {'type': 'File'},
                 'outassembly': {'type': 'File'},
                 'url': {'type': 'File'},
                 'outurl': {'type': 'File'},
                 'taxon': {'type': 'File'},
                 'outtaxon': {'type': 'File'},
                 'resource': {'type': 'File'},
                 'text': {'type': 'File'},
                 'outtext': {'type': 'File'},
                 'refseq': {'type': 'File'},
                 'outrefseq': {'type': 'File'},
                 'variation': {'type': 'File'},
                 'outvariation': {'type': 'File'},
                 'outcodon': {'type': 'File'},
                 'outdata': {'type': 'File'},
                 'outdir': {'type': 'File'},
                 'outdiscrete': {'type': 'File'},
                 'outdistance': {'type': 'File'},
                 'outfile': {'type': 'File'},
                 'outfileall': {'type': 'File'},
                 'outfreq': {'type': 'File'},
                 'outmatrix': {'type': 'File'},
                 'outmatrixf': {'type': 'File'},
                 'outproperties': {'type': 'File'},
                 'outscop': {'type': 'File'},
                 'outtree': {'type': 'File'},
                 'report': {'type': 'File'},
                 'seqout': {'type': 'File'},
                 'seqoutall': {'type': 'File'},
                 'seqoutset': {'type': 'File'},
                 'assembly': {'type': 'File'},
                 'graph': {'type': 'File'},
                 'xygraph': {'type': 'File'}}

USA_TYPE = {'type': 'record',
            'fields': [
                {'type': 'File',
                 'name': 'file'},
                {'type': ['string', 'null'],
                 'name': 'format'}
            ]}

DATATYPES_CWL['sequence'] = USA_TYPE
DATATYPES_CWL['seqall'] = USA_TYPE


NAMESPACES_AND_SCHEMAS = {'$namespaces':
                          {'dct': 'http://purl.org/dc/terms/',
                           'foaf': 'http://xmlns.com/foaf/0.1/',
                           'doap': 'http://usefulinc.com/ns/doap#',
                           'adms': 'http://www.w3.org/ns/adms#',
                           'dcat': 'http://www.w3.org/ns/dcat#',
                           'edam': 'http://edamontology.org/'},
                          '$schemas': [
                              'http://dublincore.org/2012/06/14/dcterms.rdf',
                              'http://xmlns.com/foaf/spec/20140114.rdf',
                              'http://usefulinc.com/ns/doap#',
                              'http://www.w3.org/ns/adms#',
                              'http://www.w3.org/ns/dcat.rdf',
                              'http://edamontology.org/EDAM.owl']}

INPUT_SEQUENCE_FORMATS = {format_name: SEQUENCE_FORMATS[format_name] for format_name
                          in SEQUENCE_FORMATS.keys()
                          if SEQUENCE_FORMATS[format_name].get('input') is True}
OUTPUT_SEQUENCE_FORMATS = {format_name: SEQUENCE_FORMATS[format_name] for format_name
                           in SEQUENCE_FORMATS.keys()
                           if SEQUENCE_FORMATS[format_name].get('output') is True}


def get_cwl(acd_def):
    """
    generate a CWL object from an ACD object
    :type acd_def: object
    :param acd_def: ACD object
    :return: CWL object (python dictionary)
    """
    inputs = []
    outputs = []
    parameters_count = 0
    # loop on sections
    for section in acd_def.sections:
        # loop on parameters
        for parameter in section.parameters:
            parameters_count += 1
            cwl_parameter = copy.deepcopy(DATATYPES_CWL[parameter.datatype])
            cwl_parameter['id'] = parameter.name
            cwl_parameter['label'] = parameter.attributes['information'] \
                if parameter.attributes['information'] != '' \
                else parameter.attributes['prompt']
            cwl_parameter['description'] = parameter.attributes[
                'help'] or cwl_parameter['label']
            # loop on parameter qualifiers
            for name, default_value in parameter.qualifiers.iteritems():
                qual_id = name + str(parameters_count)
                if default_value == 0:
                    cwl_qual_parameter = copy.deepcopy(
                        DATATYPES_CWL['integer'])
                elif isinstance(default_value, str):
                    cwl_qual_parameter = copy.deepcopy(DATATYPES_CWL['string'])
                elif default_value is False:
                    cwl_qual_parameter = copy.deepcopy(
                        DATATYPES_CWL['boolean'])
                cwl_qual_parameter['id'] = qual_id
                cwl_qual_parameter['label'] = name
                # cwl_qual_parameter['default'] = default_value
                if name == 'osformat':
                    cwl_qual_parameter['type'] = {'type': 'enum',
                                                  'symbols': OUTPUT_SEQUENCE_FORMATS.keys()}
                    # line below is a workaround to
                    # https://github.com/common-workflow-language/cwltool/issues/101
                    cwl_qual_parameter['type'][
                        'name'] = cwl_qual_parameter['id'] + '_type'
                if name == 'osname':
                    cwl_qual_parameter['default'] = 'output'
                    # default_format = parameter.qualifiers['osformat']
                    cwl_parameter['outputBinding'] = {'glob': '$(inputs.osformat' +
                                                      str(parameters_count) +
                                                      '==null ? (inputs.osname' +
                                                      str(parameters_count) +
                                                      ' + ".fasta") : (inputs.osname' +
                                                      str(parameters_count) +
                                                      ' + "." + inputs.osformat' +
                                                      str(parameters_count) + '))'}
                cwl_qual_parameter['inputBinding'] = {'prefix': '--' + name,
                                                      'position': len(inputs) + 1}
                # qualifiers are always optional
                cwl_qual_parameter['type'] = [
                    "null", cwl_qual_parameter['type']]
                # append qualifier to the list of accepted input formats
                inputs.append(cwl_qual_parameter)
            if DATATYPES[parameter.datatype] == INPUT:
                cwl_parameter[
                    'inputBinding'] = {'prefix': '--' + parameter.name,
                                                 'position': len(inputs) + 1}
                if not(parameter.attributes['standard'] is True
                       or parameter.attributes['parameter'] is True):
                    # define if the qualifier is mandatory
                    # based on the standard or parameter attributes
                    cwl_parameter['type'] = ["null", cwl_parameter['type']]
                # cwl_parameter['default'] = parameter.attributes['default']
                inputs.append(cwl_parameter)
            else:
                outputs.append(cwl_parameter)
    acd_cwl = {'cwlVersion': 'v1.0',
               'class': 'CommandLineTool',
               'baseCommand': [acd_def.application.name, '--auto'],
               'description': acd_def.application.attributes['documentation'],
               'requirements': [{'class': 'InlineJavascriptRequirement'}],
               'doap:homepage': 'http://emboss.sf.net',
               'inputs': inputs,
               'outputs': outputs}
    acd_cwl.update(NAMESPACES_AND_SCHEMAS)
    return acd_cwl
