"""
  main module to parse ACD files and generate CWL files
"""
import sys
import os
import argparse

from ruamel.yaml import dump
from pyparsing import ParseException

from .parser import parse_acd
from .acd import UnknownAcdPropertyException
from .acd_2_cwl import get_cwl


def main():
    """
    main function
    """
    arg_parser = argparse.ArgumentParser(description='EMBOSS ACD file parser')
    arg_parser.add_argument('files', help="ACD files to process", nargs='+')
    arg_parser.add_argument('--destination',
                            help="directory to store the CWL files to",
                            default='/tmp')
    args = arg_parser.parse_args()
    for acd_file in args.files:
        try:
            print "processing file {0}...".format(acd_file)
            acd_object = parse_acd(open(acd_file, 'r').read())
            dump(get_cwl(acd_object),
                 open(os.path.join(args.destination,
                                   os.path.basename(acd_file)+'.cwl'), 'w'),
                 default_flow_style=False)
        except ParseException as pexc:
            print "Error while parsing file {0}: {1}".format(acd_file, pexc)
        except UnknownAcdPropertyException as upexc:
            print "Error while parsing file {0}: {1}".format(acd_file,
                                                             upexc.message)

if __name__ == "__main__":
    sys.exit(main())
