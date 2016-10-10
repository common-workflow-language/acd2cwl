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

from acd2cwl.acd_2_cwl import get_cwl


@click.command()
@click.option('--outdir', help='CWL files output directory', default=os.getcwd)
@click.option('--logfile', help='log file (by default logging to stderr)')
@click.option('--loglevel', help='log level')
@click.argument('files', nargs=-1)
def build(files, outdir, logfile, loglevel):
    """
    generate CWL tool wrappers
    """
    logging.basicConfig(filename=logfile or None, level=loglevel or None)
    with click.progressbar(files, label='Generating CWL tools for ACD files') \
            as \
            acd_files:
        for acd_file in acd_files:
            try:
                logging.info("processing file {0}...".format(acd_file))
                acd_object = parse_acd(open(acd_file, 'r').read())
                dump(get_cwl(acd_object),
                     open(os.path.join(outdir,
                                       os.path.basename(
                                           acd_file) + '.cwl'), 'w'),
                     default_flow_style=False)
            except ParseException as pexc:
                logging.error("Error while parsing file {0}: {1}".format(
                    acd_file, pexc))
                logging.exception(pexc)
            except UnknownAcdPropertyException as upexc:
                logging.error(
                    "Error while parsing file {0}: {1}".format(acd_file,
                                                               upexc.message))
                logging.exception(upexc)

if __name__ == '__main__':
    build()
