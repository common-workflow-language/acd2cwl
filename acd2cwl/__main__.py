"""
  main module to parse ACD files and generate CWL files
"""
import sys
import os
import argparse
import logging

from ruamel.yaml import dump
from pyparsing import ParseException

from pyacd.parser import parse_acd
from pyacd.acd import UnknownAcdPropertyException
from pyacd.qaparser import parse_qa

from .acd_2_cwl import get_cwl, DATATYPES_CWL

def parse_tools(args):
    """
    subcommand to generate CWL tool wrappers
    :param args:
    :return:
    """
    for acd_file in args.files:
        try:
            logging.info("processing file {0}...".format(acd_file))
            acd_object = parse_acd(open(acd_file, 'r').read())
            dump(get_cwl(acd_object),
                 open(os.path.join(args.outdir,
                                   os.path.basename(acd_file)+'.cwl'), 'w'),
                 default_flow_style=False)
        except ParseException as pexc:
            logging.error("Error while parsing file {0}: {1}".format(
                acd_file, pexc))
            logging.exception(pexc)
        except UnknownAcdPropertyException as upexc:
            logging.error("Error while parsing file {0}: {1}".format(acd_file,
                                                             upexc.message))
            logging.exception(upexc)

def parse_tests(args):
    """
    subcommand to generate cwltool job orders
    :param args:
    :return:
    """
    acd_reference = {}
    for acd_file in args.files:
        try:
            acd_object = parse_acd(open(acd_file, 'r').read())
            acd_reference[acd_object.application.name] = acd_object
        except ParseException as pexc:
            logging.error("Error while parsing file {0}: {1}".format(acd_file,
                                                                  pexc))
            logging.exception(pexc)
        except UnknownAcdPropertyException as upexc:
            logging.error("Error while parsing file {0}: {1}".format(acd_file,
                                                         upexc.message))
            logging.exception(upexc)
    qa_tests_string = ''
    for qaline in open(args.qatestfile, 'r').readlines():
        if not(qaline.startswith('#')):
            qa_tests_string += qaline
    qa_tests_array = qa_tests_string.split('//\n\n')
    for qa_test_string in qa_tests_array:
        if qa_test_string.strip()=='':
            #ignore empty chunks
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
                if DATATYPES_CWL[parameter.datatype].get('type')=='File':
                    cwl_job_order[key]={'class':'File',
                                        'path':job_order[key]['value']}
                else:
                    cwl_job_order[key] = job_order[key]['value']
                for qualifier in job_order[key].keys():
                    if qualifier=='value':
                        continue
                    cwl_job_order[qualifier]= job_order[key][qualifier]
            logging.info("writing test job order {0} for tool {1}".format(
                qa_test.id, qa_test.application_ref.name))
            dump(cwl_job_order, open(os.path.join(args.outdir,
                                                    os.path.basename(
                                                        qa_test.id) + '.yml'),
                                       'w'), default_flow_style=False)
        except Exception as exc:
            logging.error("QA test parsing failed for:\n{0}".format(
                qa_test_string))
            logging.exception(exc)

def main():
    """
    main function
    """
    arg_parser = argparse.ArgumentParser(description='EMBOSS ACD file parser')
    arg_parser.add_argument('files', help="ACD files to process", nargs='+')
    subparsers = arg_parser.add_subparsers(help='sub-command help')
    parser_tools = subparsers.add_parser('tools', help='parse ACD files '
                                                           'and '
                                                  'generate CWL tools'
                                           'files')
    parser_tools.add_argument('--outdir',
                            help="CWL files directory",
                            default='/tmp')
    parser_tools.set_defaults(func=parse_tools)

    parser_tests = subparsers.add_parser('tests', help='parse QA file '
                                                 'and generate job order '
                                                 'values files')
    parser_tests.add_argument('--qatestfile', help='path to the QA test files '
                                                 'to be parsed to generate '
                                                 'the CWL job orders')
    parser_tests.add_argument('--outdir',
                              help="job order files files directory",
                              default='/tmp')
    parser_tests.set_defaults(func=parse_tests)
    args = arg_parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    sys.exit(main())
