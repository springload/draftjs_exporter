from __future__ import absolute_import, unicode_literals

import re
import unittest
from draftjs_exporter.html import HTML
from draftjs_exporter.composite_decorators import CompositeDecorator, URLDecorator


class HashTagDecorator(CompositeDecorator):
    SEARCH_RE = re.compile(r'#\w+')

    def replace(self, match):
        return '<span class="hash_tag">{hash_tag}</span>'.format(
            hash_tag=match.group(0) or '')


config = {
    'entity_decorators': {},
    'composite_decorators': [
        URLDecorator(),
        HashTagDecorator()
    ],
    'block_map': {
        'unstyled': {'element': 'div'}
    },
    'style_map': {
        'ITALIC': {'element': 'em'},
        'BOLD': {'element': 'strong'}
    }
}


class TestCompositeDecorator(unittest.TestCase):

    def setUp(self):
        self.exporter = HTML(config)

    def test_render_with_composite_decorator(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'search https://yahoo.com or www.google.com for #github and #facebook',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ]
        }),
            '<div>search <a href="https://yahoo.com">https://yahoo.com</a>'
            ' or <a href="http://www.google.com">www.google.com</a>'
            ' for <span class="hash_tag">#github</span> and '
            '<span class="hash_tag">#facebook</span></div>')
