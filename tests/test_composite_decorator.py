from __future__ import absolute_import, unicode_literals

import re
import unittest
from draftjs_exporter.html import HTML
from draftjs_exporter.composite_decorators import CompositeDecorator, URLDecorator
from draftjs_exporter.entities import Link


class HashTagDecorator(CompositeDecorator):
    SEARCH_RE = re.compile(r'#\w+')

    def replace(self, match):
        return '<span class="hash_tag">{hash_tag}</span>'.format(
            hash_tag=match.group(0) or '')


config = {
    'entity_decorators': {
        'LINK': Link()
    },
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
            'entityMap': {
                '1': {
                    'type': 'LINK',
                    'mutability': 'MUTABLE',
                    'data': {
                        'url': 'http://amazon.us'
                    }
                }
            },
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'search http://a.us or https://yahoo.com or www.google.com for #github and #facebook',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': [
                        {
                            'offset': 7,
                            'length': 11,
                            'key': 1
                        }
                    ],
                },
            ]
        }),
            '<div>search <a href="http://amazon.us">http://a.us</a> or '
            '<a href="https://yahoo.com">https://yahoo.com</a> or '
            '<a href="http://www.google.com">www.google.com</a> for '
            '<span class="hash_tag">#github</span> and '
            '<span class="hash_tag">#facebook</span></div>')
