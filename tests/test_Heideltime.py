
import unittest

from python_heideltime import Heideltime


class TestHeideltime(unittest.TestCase):

    def test__convert_to_json(self):
        heideltime = Heideltime()
        heideltime.set_output_type('JSON')

        self.assertEqual('TIMEML', heideltime.output_type)

        test_text = 'Yesterday we drove to the mountains. Today we are going to the sea'

        result = heideltime.parse(test_text)

        expected_result = [
            {
                'tid': 't1',
                'type': 'DATE',
                'value': 'XXXX-XX-XX',
                'text': 'Yesterday',
                'char_pos': [0, 9]
            },
            {
                'tid': 't2',
                'type': 'DATE',
                'value': 'PRESENT_REF',
                'text': 'Today',
                'char_pos': [37, 42]
            }
        ]

        self.assertEqual(expected_result, result)
