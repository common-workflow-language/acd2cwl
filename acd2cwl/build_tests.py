"""
  main module to parse ACD files and generate CWL files
"""
import os
import logging

from ruamel.yaml import dump
from pyparsing import ParseException
import click

from pyacd.parser import parse_acd
from pyacd.acd import UnknownAcdPropertyException
from pyacd.qaparser import parse_qa

from acd2cwl.acd_2_cwl import DATATYPES_CWL


@click.command()
@click.option('--outdir', help='test job files output directory')
@click.option('--logfile', help='log file (by default logging to stderr)')
@click.option('--loglevel', help='log level')
@click.option('--qatestfile', help='test job files output directory')
@click.argument('files', nargs=-1)
def build(files, outdir, logfile, loglevel, qatestfile):
    """
    subcommand to generate cwltool job orders from EMBOSS QA file
    """
    logging.basicConfig(filename=logfile or None, level=loglevel or None)
    with click.progressbar(files, label='Loading ACD files') \
            as acd_files:
        acd_reference = {}
        for acd_file in acd_files:
            try:
                acd_object = parse_acd(open(acd_file, 'r').read())
                acd_reference[acd_object.application.name] = acd_object
            except ParseException as pexc:
                logging.error(
                    "Error while parsing file {0}: {1}".format(acd_file,
                                                               pexc))
                logging.exception(pexc)
            except UnknownAcdPropertyException as upexc:
                logging.error(
                    "Error while parsing file {0}: {1}".format(acd_file,
                                                               upexc.message))
                logging.exception(upexc)
    with click.progressbar(open(qatestfile, 'r').readlines(),
                           label='Preprocessing QA file') \
            as qa_lines:
        qa_tests_string = ''
        for qa_line in qa_lines:
            if not(qa_line.startswith('#')):
                qa_tests_string += qa_line

    qa_tests_array = qa_tests_string.split('//\n\n')
    with click.progressbar(qa_tests_array, label='Generating job order '
                                                 'files for QA tests') as \
            qa_tests_array_progress:
        for qa_test_string in qa_tests_array_progress:
            if qa_test_string.strip() == '':
                # ignore empty chunks
                continue
            try:
                qa_test = parse_qa(qa_test_string)
                if qa_test.application_ref.name not in acd_reference:
                    continue
                job_order = qa_test.parse_command_lines(acd_reference[
                    qa_test.application_ref.name])
                cwl_job_order = {}
                for key in job_order.keys():
                    parameter = acd_reference[
                        qa_test.application_ref.name].parameter_by_name(key)
                    if DATATYPES_CWL[parameter.datatype].get('type') == 'File':
                        cwl_job_order[key] = {'class': 'File',
                                              'path': job_order[key]['value']}
                    else:
                        cwl_job_order[key] = job_order[key]['value']
                    for qualifier in job_order[key].keys():
                        if qualifier == 'value':
                            continue
                        cwl_job_order[qualifier] = job_order[key][qualifier]
                logging.info("writing test job order {0} for tool {1}".format(
                    qa_test.id, qa_test.application_ref.name))
                dump(
                    cwl_job_order, open(
                        os.path.join(
                            outdir, os.path.basename(
                                qa_test.id) + '.yml'), 'w'),
                     default_flow_style=False)
            except Exception as exc:
                logging.error("QA test parsing failed for:\n{0}".format(
                    qa_test_string))
                logging.exception(exc)

if __name__ == '__main__':
    build()
