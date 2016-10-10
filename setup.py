#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os.path

SETUP_DIR = os.path.dirname(__file__)
README = os.path.join(SETUP_DIR, 'README.md')
readme = open(README).read()

setup(
    name='acd2cwl',
    version='0.1.1',
    description='CWL generator for ACD files',
    long_description=readme,
    keywords=['EMBOSS','ACD','Common Workflow Language', 'CWL'],
    author='Hervé Ménager',
    author_email='hmenager@pasteur.fr',
    url='https://github.com/hmenager/acd2cwl',
    download_url='https://github.com/hmenager/acd2cwl',
    packages=['acd2cwl'],
    install_requires=[
        'click',
        'ruamel.yaml',
        'pyacd'
    ],
    license="BSD",
    entry_points={
          'console_scripts': ['a2c-tools=acd2cwl.build_tools:build',
                              'a2c-tests=acd2cwl.build_tests:build'],
        },
    tests_require=['nose'],
    test_suite='nose.collector',
    include_package_data=True,
    zip_safe=False
)
