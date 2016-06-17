import sys
import os
import argparse
import glob

from yaml import dump
from pyparsing import ParseException

from .parser import AcdParser
from .acd import UnknownAcdPropertyException
from .acd_2_cwl import get_cwl, print_datatype_parameter_class_mapping

def main():
    arg_parser = argparse.ArgumentParser(description='EMBOSS ACD file parser')
    arg_parser.add_argument('--files', help="ACD files to process")
    arg_parser.add_argument('--destination', help="directory to store the CWL files to")
    args = arg_parser.parse_args()
    parser = AcdParser()
    for file in glob.glob(args.files):
        try:
            print "processing file {0}...".format(file)
            acd_object = parser.parse_acd(open(file,'r').read())
            dump(get_cwl(acd_object), open(os.path.join(args.destination, os.path.basename(file)+'.cwl'),'w'),
                       default_flow_style=False)
        except ParseException as pexc:
            print "Error while parsing file {0}: {1}".format(file, pexc)
        except UnknownAcdPropertyException as upexc:
            print "Error while parsing file {0}: {1}".format(file, upexc.message)

if __name__ == "__main__":
    #print_datatype_parameter_class_mapping()
    sys.exit(main())