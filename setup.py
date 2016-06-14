#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
from setuptools import setup

readme = open('README.md').read()

setup(
    name='pyacd',
    version='0.1',
    description='python API to EMBOSS ACD files',
    long_description=readme,
    author='Hervé Ménager',
    author_email='hmenager@pasteur.fr',
    url='https://github.com/hmenager/pyacd.git',
    packages=['pyacd'],
    install_requires=[
          'pyparsing'
    ],
    license="BSD",
    entry_points={
          'console_scripts': ['pyacd=pyacd:main'],
        },
    include_package_data=True,
    zip_safe=False 
)
