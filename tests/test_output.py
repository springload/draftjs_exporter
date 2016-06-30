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
        'BOLD': {'fontStyle': 'bold'},
        'HIGHLIGHT': {'fontStyle': 'bold', 'textDecoration': 'underline'},
    }
}


class TestOutput(unittest.TestCase):
    def setUp(self):
        self.exporter = HTML(config)
        self.test_cases = json.loads(codecs.open(fixtures_path, 'r', 'utf-8').read())

    def test_call_with_different_blocks_decodes(self):
        # TODO Was <div><h1>Header</h1><div>some paragraph text</div></div>
        # Which behaviour do we want here?
        self.assertEqual(self.exporter.call({
            'entityMap': {},
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'Header',
                    'type': 'header-one',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                }
            ]
        }), '<h1>Header</h1><div>some paragraph text</div>')

    def test_call_with_inline_styles_decodes(self):
        self.assertEqual(self.exporter.call({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'ITALIC'
                        }
                    ],
                    'entityRanges': []
                }
            ]
        }), '<div><span style="font-style: italic;">some</span> paragraph text</div>')

    def test_call_with_multiple_inline_styles_decodes(self):
        self.assertEqual(self.exporter.call({
            'entityMap': {},
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'Header',
                    'type': 'header-one',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 2,
                            'style': 'BOLD'
                        }
                    ],
                    'entityRanges': []
                },
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'HIGHLIGHT'
                        }
                    ],
                    'entityRanges': [
                        {
                            'offset': 5,
                            'length': 9,
                            'key': 0
                        }
                    ]
                }
            ]
        }), '<h1><span style="font-style: bold;">He</span>ader</h1><div><span style="font-style: bold;text-decoration: underline;">some</span> paragraph text</div>')

    @unittest.skip('TODO')
    def test_call_with_entities_decodes(self):
        self.assertEqual(self.exporter.call({
            'entityMap': {
                '0': {
                    'type': 'LINK',
                    'mutability': 'MUTABLE',
                    'data': {
                        'url': 'http://example.com'
                    }
                }
            },
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': [
                        {
                            'offset': 5,
                            'length': 9,
                            'key': 0
                        }
                    ]
                }
            ]
        }), '<div>some <a href="http://example.com">paragraph</a> text</div>')

    @unittest.skip('TODO')
    def test_call_with_entities_crossing_throws(self):
        with self.assertRaises(ValueError):
            self.exporter.call({
                'entityMap': {
                    '0': {
                        'type': 'LINK',
                        'mutability': 'MUTABLE',
                        'data': {
                            'url': 'http://example.com'
                        }
                    },
                    '1': {
                        'type': 'LINK',
                        'mutability': 'MUTABLE',
                        'data': {
                            'url': 'http://bar.example.com'
                        }
                    }
                },
                'blocks': [
                    {
                        'key': 'dem5p',
                        'text': 'some paragraph text',
                        'type': 'unstyled',
                        'depth': 0,
                        'inlineStyleRanges': [],
                        'entityRanges': [
                            {
                                'offset': 5,
                                'length': 9,
                                'key': 0
                            },
                            {
                                'offset': 2,
                                'length': 9,
                                'key': 1
                            }
                        ]
                    }
                ]
            })

    def test_call_with_wrapped_blocks(self):
        self.assertEqual(self.exporter.call({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': [],
                },
                {
                    'key': 'dem5p',
                    'text': 'item2',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                }
            ]
        }), '<ul class="public-DraftStyleDefault-ul"><li>item1</li><li>item2</li></ul>')

    # TODO Find a way to have one test case per case in the JSON file
    @unittest.skip('TODO')
    def test_cases(self):
        for case in self.test_cases:
            self.assertEqual(self.exporter.call(case.get('content_state')), case.get('output'))
