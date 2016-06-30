import codecs
import json
import os
import unittest

from draftjs_exporter.entities.link import Link
from draftjs_exporter.html import HTML

fixtures_path = os.path.join(os.path.dirname(__file__), 'test_exports.json')
fixtures = json.loads(codecs.open(fixtures_path, 'r', 'utf-8').read())

config = {
    'entity_decorators': {
        'LINK': Link()
    },
    'block_map': {
        'header-one': {'element': 'h1'},
        'unordered-list-item': {
            'element': 'li',
            'wrapper': ['ul', {'className': 'public-DraftStyleDefault-ul'}]
        },
        'unstyled': {'element': 'p'}
    },
    'style_map': {
        'ITALIC': {'fontStyle': 'italic'},
        'BOLD': {'fontStyle': 'bold'},
        'HIGHLIGHT': {'fontStyle': 'bold', 'textDecoration': 'underline'},
    }
}


class TestExports(unittest.TestCase):
    # TODO Find a way to have one test case per case in the JSON file
    @unittest.skip('TODO')
    def test_exports(self):
        for export in fixtures:
            exporter = HTML(config)
            self.assertEqual(exporter.call(export.get('content_state')), export.get('output'))
