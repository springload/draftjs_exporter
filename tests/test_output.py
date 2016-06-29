import codecs
import json
import os
import unittest

from draft_exporter.entities.link import Link
from draft_exporter.html import HTML

fixtures_path = os.path.join(os.path.dirname(__file__), 'test_cases.json')

config = {
    'entity_decorators': {
        'LINK': Link
    },
    'block_map': {
        'header-one': {'element': 'h1'},
        'unordered-list-item': {
            'element': 'li',
            'wrapper': ['ul', {'className': 'public-DraftStyleDefault-ul'}]
        },
        'unstyled': {'element': 'div'}
    },
    'style_map': {
        'ITALIC': {'fontStyle': 'italic'},
        'BOLD': {'fontStyle': 'bold'}
    }
}


class TestOutput(unittest.TestCase):
    def setUp(self):
        self.exporter = HTML(config)
        self.test_cases = json.loads(codecs.open(fixtures_path, 'r', 'utf-8').read())

    ## TODO Find a way to have one test case per case in the JSON file
    @unittest.skip('TODO')
    def test_cases(self):
        for case in self.test_cases:
            self.assertEqual(self.exporter.call(case.get('content_state')), case.get('output'))
