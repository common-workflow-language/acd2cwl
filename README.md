CWL generator for ACD (EMBOSS) files.
=====================================

acd2cwl provides:
- a2c-tools, a generator of wrappers for EMBOSS tools. It uses the formal definition of the tools provided by the ACD files.
- a2c-tests, a generator of functional tests for these tools. It uses the functional tests defined in the EMBOSS package itself

Install
-------

Installing the official package from PyPi:

`pip install acd2cwl`

Or from source:
`
git clone https://github.com/hmenager/acd2cwl.git
cd acd2cwl && python setup.py install
`

Run tool wrappers generator
---------------------------

Simple command:

`a2c-tools /usr/share/EMBOSS/acd/*.acd`

For more options, just type

`a2c-tools --help`

Run test jobs generator
-----------------------

Simple command:

`a2c-tests /usr/share/EMBOSS/test/qatest.dat /usr/share/EMBOSS/acd/*.acd`

For more options, just type

`a2c-tests --help`
