import unittest
from pyacd.parser import parse_attribute, parse_attributes, parse_parameter, \
    parse_parameters, parse_section, parse_sections, parse_application, parse_acd
from pyacd import acd

class TestParser(unittest.TestCase):

    # def setUp(self):
    #     #instanciate parser
    #     self.parser = AcdParser()

    def test_parse_attribute(self):
        attribute = parse_attribute('documentation: "Read and write (return) sequences"')
        self.assertEqual(attribute.name, 'documentation')
        self.assertEqual(attribute.value,'Read and write (return) sequences')

    def test_parse_attributes_list(self):
        attributes_list = parse_attributes("""
            groups: "Data retrieval, Edit"
            relations: "EDAM_topic:0090 Data search and retrieval"
            relations: "EDAM_operation:1813 Sequence retrieval"
            relations: "EDAM_operation:2121 Sequence file processing"
        """)
        self.assertEqual(attributes_list[0].name, 'groups')
        self.assertEqual(attributes_list[0].value, 'Data retrieval, Edit')
        self.assertEqual(attributes_list[1].name, 'relations')
        self.assertEqual(attributes_list[1].value, 'EDAM_topic:0090 Data search and retrieval')

    def test_parse_parameter(self):
        parameter = parse_parameter("""
            string: myparameter [
            information: "parameter information"
            prompt: "test prompt"
            needed: "yes"
            additional: "no"
        ]""")
        self.assertEqual(parameter.name, 'myparameter')
        self.assertEqual(parameter.attributes['information'], 'parameter information')
        self.assertEqual(parameter.attributes['prompt'], 'test prompt')

    def test_parse_boolean_values(self):
        parameter = parse_parameter("""
            string: myparameter [
            needed: "yes"
            additional: "no"
        ]""")
        self.assertEqual(parameter.attributes['needed'], True)
        self.assertEqual(parameter.attributes['additional'], False)
        parameter = parse_parameter("""
            string: myparameter [
            needed: "Y"
            additional: "N"
        ]""")
        self.assertEqual(parameter.attributes['needed'], True)
        self.assertEqual(parameter.attributes['additional'], False)
        parameter = parse_parameter("""
            string: myparameter [
            needed: "y"
            additional: "n"
        ]""")
        self.assertEqual(parameter.attributes['needed'], True)
        self.assertEqual(parameter.attributes['additional'], False)
        parameter = parse_parameter("""
            string: myparameter [
            needed: "true"
            additional: "false"
        ]""")
        self.assertEqual(parameter.attributes['needed'], True)
        self.assertEqual(parameter.attributes['additional'], False)
        def bad_value_parse():
            parse_parameter("""
                string: myparameter [
                needed: "W"
            ]""")
        self.assertRaises(acd.InvalidAcdPropertyValue, bad_value_parse)

    def test_parse_parameters(self):
        parameters_list = parse_parameters("""
        string: myparameter [
            information: "parameter information"
        ]

        string: myparameterZ [
            information: "parameter 2 information"
        ]
        """)
        self.assertEqual(len(parameters_list),2)
        self.assertIsInstance(parameters_list[0], acd.Parameter)
        self.assertIsInstance(parameters_list[1], acd.Parameter)

    def test_parse_section(self):
        section = parse_section("""
        section: input [
              information: "Input section"
              type: "page"
            ]

              boolean: feature [
                information: "Use feature information"
                relations: "EDAM_data:2527 Parameter"
              ]

              seqall: sequence [
                parameter: "Y"
                type: "gapany"
                features: "$(feature)"
                relations: "EDAM_data:0849 Sequence record"
              ]

            endsection: input
        """)
        self.assertEqual(section.name,"input")

    def test_parse_application(self):
        application = parse_application("""
            application: seqret [
              documentation: "Read and write (return) sequences"
              groups: "Data retrieval, Edit"
                relations: "EDAM_topic:0090 Data search and retrieval"
                relations: "EDAM_operation:1813 Sequence retrieval"
                relations: "EDAM_operation:2121 Sequence file processing"
            ]
        """)
        self.assertEqual(application.name, "seqret")
        self.assertEqual(application.attributes['documentation'], 'Read and write (return) sequences')
        self.assertEqual(application.attributes['groups'], 'Data retrieval, Edit')
        self.assertEqual(application.attributes['relations'], ['EDAM_topic:0090 Data search and retrieval',
                                                               'EDAM_operation:1813 Sequence retrieval',
                                                               'EDAM_operation:2121 Sequence file processing'])

    def test_parse_acd(self):
        my_acd = parse_acd("""
        application: seqret [
          documentation: "Read and write (return) sequences"
          groups: "Data retrieval, Edit"
            relations: "EDAM_topic:0090 Data search and retrieval"
            relations: "EDAM_operation:1813 Sequence retrieval"
            relations: "EDAM_operation:2121 Sequence file processing"
        ]

        section: input [
          information: "Input section"
          type: "page"
        ]

          boolean: feature [
            information: "Use feature information"
            relations: "EDAM_data:2527 Parameter"
          ]

          seqall: sequence [
            parameter: "Y"
            type: "gapany"
            features: "$(feature)"
            relations: "EDAM_data:0849 Sequence record"
          ]

        endsection: input

        section: advanced [
          information: "Advanced section"
          type: "page"
        ]

          boolean: firstonly [
            default: "N"
            information: "Read one sequence and stop"
            relations: "EDAM_data:2527 Parameter"
          ]

        endsection: advanced

        section: output [
          information: "Output section"
          type: "page"
        ]

          seqoutall: outseq [
            parameter: "Y"
            features: "$(feature)"
            relations: "EDAM_data:0849 Sequence record"
          ]

        endsection: output
        """)
        self.assertEqual(my_acd.application.name, "seqret")
        self.assertEqual(len(my_acd.sections), 3)
        self.assertEqual(my_acd.sections[0].name, "input")
        self.assertEqual(my_acd.sections[1].name, "advanced")
        self.assertEqual(my_acd.sections[2].name, "output")
