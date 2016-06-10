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
                 'range': {'type': 'file'},
                 'regexp': {'type': 'file'},
                 'pattern': {'type': 'file'},
                 'string': {'type': 'string'},
                 'toggle': {'type': 'file'},
                 'codon': {'type': 'file'},
                 'cpdb': {'type': 'file'},
                 'datafile': {'type': 'file'},
                 'directory': {'type': 'file'},
                 'dirlist': {'type': 'file'},
                 'discretestates': {'type': 'file'},
                 'distances': {'type': 'file'},
                 'features': {'type': 'file'},
                 'filelist': {'type': 'file'},
                 'frequencies': {'type': 'file'},
                 'infile': {'type': 'file'},
                 'matrix': {'type': 'file'}, 'matrixf': {'type': 'file'},
                 'properties': {'type': 'file'},
                 'scop': {'type': 'file'}, 'sequence': {'type': 'file'}, 'seqall': {'type': 'file'},
                 'seqset': {'type': 'file'}, 'seqsetall': {'type': 'file'},
                 'tree': {'type': 'file'},
                 'list': {'type': 'file'}, 'selection': {'type': 'file'},
                 'align': {'type': 'file'}, 'featout': {'type': 'file'}, 'outcodon': {'type': 'file'},
                 'outdata': {'type': 'file'}, 'outdir': {'type': 'file'},
                 'outdiscrete': {'type': 'file'},
                 'outdistance': {'type': 'file'},
                 'outfile': {'type': 'file'}, 'outfileall': {'type': 'file'}, 'outfreq': {'type': 'file'},
                 'outmatrix': {'type': 'file'},
                 'outmatrixf': {'type': 'file'}, 'outproperties': {'type': 'file'},
                 'outscop': {'type': 'file'}, 'outtree': {'type': 'file'}, 'report': {'type': 'file'},
                 'seqout': {'type': 'file'}, 'seqoutall': {'type': 'file'},
                 'seqoutset': {'type': 'file'},
                 'graph': {'type': 'file'}, 'xygraph': {'type': 'file'}}


def get_cwl(acdDef):
    inputs = []
    outputs = []
    for section in acdDef.sections:
        for parameter in section.parameters:
            cwl_parameter = copy.deepcopy(DATATYPES_CWL[parameter.datatype])
            cwl_parameter['id'] = parameter.name
            if DATATYPES[parameter.datatype] == 'input':
                cwl_parameter['inputBinding'] = {'prefix': '--' + parameter.name,
                                                 'position': len(inputs) + 1}
                inputs.append(cwl_parameter)
            else:
                cwl_parameter['outputBinding'] = {}
                outputs.append(cwl_parameter)
    return {'cwlVersion': 'cwl:draft3',
            'class': 'CommandLineTool',
            'baseCommand': acdDef.application.name,
            'description': acdDef.application.attributes['documentation'],
            'inputs': inputs,
            'outputs': outputs
            }


def print_datatype_parameter_class_mapping():
    for datatype in DATATYPES:
        print
        datatype, parameterClasses.get(datatype, None)
