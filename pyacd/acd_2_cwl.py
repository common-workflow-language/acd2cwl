import copy

from .acd import parameterClasses

DATATYPES = {'array': 'input',
             'boolean': 'input',
             'integer': 'input',
             'float': 'input',
             'range': 'input',
             'regexp': 'input',
             'pattern': 'input',
             'string': 'input',
             'toggle': 'input',
             'codon': 'input',
             'cpdb': 'input',
             'datafile': 'input',
             'directory': 'input',
             'dirlist': 'input',
             'discretestates': 'input',
             'distances': 'input',
             'features': 'input',
             'filelist': 'input',
             'frequencies': 'input',
             'infile': 'input', 'matrix': 'input', 'matrixf': 'input',
             'properties': 'input',
             'scop': 'input', 'sequence': 'input', 'seqall': 'input', 'seqset': 'input', 'seqsetall': 'input',
             'tree': 'input',
             'list': 'input', 'selection': 'input',
             'align': 'output', 'featout': 'output', 'outcodon': 'output', 'outdata': 'output', 'outdir': 'output',
             'outdiscrete': 'output',
             'outdistance': 'output',
             'outfile': 'output', 'outfileall': 'output', 'outfreq': 'output', 'outmatrix': 'output',
             'outmatrixf': 'output', 'outproperties': 'output',
             'outscop': 'output', 'outtree': 'output', 'report': 'output', 'seqout': 'output', 'seqoutall': 'output',
             'seqoutset': 'output',
             'graph': 'output', 'xygraph': 'output'}

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
                 'matrix': {'type': 'File'}, 'matrixf': {'type': 'File'},
                 'properties': {'type': 'File'},
                 'scop': {'type': 'File'}, 'sequence': {'type': 'File'}, 'seqall': {'type': 'File'},
                 'seqset': {'type': 'File'}, 'seqsetall': {'type': 'File'},
                 'tree': {'type': 'File'},
                 'list': {'type': 'File'}, 'selection': {'type': 'File'},
                 'align': {'type': 'File'}, 'featout': {'type': 'File'}, 'outcodon': {'type': 'File'},
                 'outdata': {'type': 'File'}, 'outdir': {'type': 'File'},
                 'outdiscrete': {'type': 'File'},
                 'outdistance': {'type': 'File'},
                 'outfile': {'type': 'File'}, 'outfileall': {'type': 'File'}, 'outfreq': {'type': 'File'},
                 'outmatrix': {'type': 'File'},
                 'outmatrixf': {'type': 'File'}, 'outproperties': {'type': 'File'},
                 'outscop': {'type': 'File'}, 'outtree': {'type': 'File'}, 'report': {'type': 'File'},
                 'seqout': {'type': 'File'}, 'seqoutall': {'type': 'File'},
                 'seqoutset': {'type': 'File'},
                 'graph': {'type': 'File'}, 'xygraph': {'type': 'File'}}

NAMESPACES_AND_SCHEMAS = {'$namespaces': {
  'dct': 'http://purl.org/dc/terms/',
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
    'http://edamontology.org/EDAM.owl']
}

def get_cwl(acdDef):
    inputs = []
    outputs = []
    parameters_count = 0
    #loop on sections
    for section in acdDef.sections:
        #loop on parameters
        for parameter in section.parameters:
            parameters_count += 1
            cwl_parameter = copy.deepcopy(DATATYPES_CWL[parameter.datatype])
            cwl_parameter['id'] = parameter.name
            cwl_parameter['label'] = parameter.attributes['information'] if parameter.attributes['information']!='' else parameter.attributes['prompt']
            cwl_parameter['description'] = parameter.attributes['help'] or cwl_parameter['label']
            #loop on parameter qualifiers
            for name, default_value in parameter.qualifiers.iteritems():
                qual_id = name + str(parameters_count)
                if default_value==0:
                    cwl_qual_parameter = copy.deepcopy(DATATYPES_CWL['integer'])
                elif type(default_value)==str:
                    cwl_qual_parameter = copy.deepcopy(DATATYPES_CWL['string'])
                elif default_value==False:
                    cwl_qual_parameter = copy.deepcopy(DATATYPES_CWL['boolean'])
                #qualifiers are always optional
                cwl_qual_parameter['type'] = ["null", cwl_qual_parameter['type']]
                cwl_qual_parameter['id'] = qual_id
                cwl_qual_parameter['label'] = name
                #cwl_qual_parameter['default'] = default_value
                if name=='osname':
                    cwl_qual_parameter['default'] = 'output'
                    default_format = parameter.qualifiers['osformat']
                    cwl_parameter['outputBinding'] = {'glob':'$(inputs.osformat' + str(parameters_count) +
                                                             '==null ? (inputs.osname' + str(parameters_count) +
                                                             ' + ".fasta") : (inputs.osname' + str(parameters_count) +
                                                             ' + "." + inputs.osformat' + str(parameters_count) + '))'}
                cwl_qual_parameter['inputBinding'] = {'prefix': '--' + name,
                                                 'position': len(inputs) + 1}
                inputs.append(cwl_qual_parameter)
            if DATATYPES[parameter.datatype] == 'input':
                cwl_parameter['inputBinding'] = {'prefix': '--' + parameter.name,
                                                 'position': len(inputs) + 1}
                if not(parameter.attributes['standard']==True or parameter.attributes['parameter']==True):
                    # define if the qualifier is mandatory based on the standard or parameter attributes
                    cwl_parameter['type'] = ["null", cwl_parameter['type']]
                #cwl_parameter['default'] = parameter.attributes['default']
                inputs.append(cwl_parameter)
            else:
                outputs.append(cwl_parameter)
    acd_cwl = {'cwlVersion': 'cwl:draft-3',
            'class': 'CommandLineTool',
            'baseCommand': [acdDef.application.name, '--auto'],
            'description': acdDef.application.attributes['documentation'],
            'requirements': [{'class': 'InlineJavascriptRequirement'}],
            'inputs': inputs,
            'outputs': outputs
            }
    acd_cwl.update(NAMESPACES_AND_SCHEMAS)
    return acd_cwl


def print_datatype_parameter_class_mapping():
    for datatype in DATATYPES:
        print
        datatype, parameterClasses.get(datatype, None)
