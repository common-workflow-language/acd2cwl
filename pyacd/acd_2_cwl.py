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
    for section in acdDef.sections:
        for parameter in section.parameters:
            cwl_parameter = copy.deepcopy(DATATYPES_CWL[parameter.datatype])
            cwl_parameter['id'] = parameter.name
            cwl_parameter['label'] = parameter.attributes['information'] if parameter.attributes['information']!='' else parameter.attributes['prompt']
            cwl_parameter['description'] = parameter.attributes['help'] or cwl_parameter['label']
            if DATATYPES[parameter.datatype] == 'input':
                cwl_parameter['inputBinding'] = {'prefix': '--' + parameter.name,
                                                 'position': len(inputs) + 1}
                cwl_parameter['default'] = parameter.attributes['default']
                inputs.append(cwl_parameter)
            else:
                cwl_parameter['outputBinding'] = {}
                outputs.append(cwl_parameter)
    acd_cwl = {'cwlVersion': 'cwl:draft-3',
            'class': 'CommandLineTool',
            'baseCommand': acdDef.application.name,
            'description': acdDef.application.attributes['documentation'],
            'inputs': inputs,
            'outputs': outputs
            }
    acd_cwl.update(NAMESPACES_AND_SCHEMAS)
    return acd_cwl


def print_datatype_parameter_class_mapping():
    for datatype in DATATYPES:
        print
        datatype, parameterClasses.get(datatype, None)
