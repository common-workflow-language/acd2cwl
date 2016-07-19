import unittest
from pyacd.qaparser import QAParser

class TestParser(unittest.TestCase):

    def setUp(self):
        #instanciate parser
        self.parser = QAParser()

    def test_parse_cl_parameter(self):
        res = self.parser.parse_cl_parameter("-sequence test.fasta")
        self.assertEqual(res.name, 'sequence')
        self.assertEqual(res.value, 'test.fasta')

    def test_parse_cl_parameter_noname(self):
        # parameter with no name specified
        res = self.parser.parse_cl_parameter("test.fasta")
        self.assertEqual(res.name, '')
        self.assertEqual(res.value, 'test.fasta')

    def test_parse_cl_parameters(self):
        res = self.parser.parse_cl_parameters("-sequence test -osformat genbank")
        self.assertEqual(res.parameters[0].parameter.name, 'sequence')
        self.assertEqual(res.parameters[0].parameter.value, 'test')
        self.assertEqual(res.parameters[1].parameter.name, 'osformat')
        self.assertEqual(res.parameters[1].parameter.value, 'genbank')

    def test_parse_test(self):
        res = self.parser.parse_test("""
        ID qual-ufo
        AP seqret
        CL bam::../../data/samspec1.4example.bam -osformat sam stdout -auto
        """)
        self.assertEqual(res.id, 'qual-ufo')
        self.assertEqual(res.application, 'seqret')
        self.assertEqual(res.commandline[0].parameter.name, '')
        self.assertEqual(res.commandline[0].parameter.value, 'bam::../../data/samspec1.4example.bam')
        self.assertEqual(res.commandline[1].parameter.name, 'osformat')
        self.assertEqual(res.commandline[1].parameter.value, 'sam')
