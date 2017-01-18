from __future__ import absolute_import, unicode_literals

import cgi
import re
import unittest

from draftjs_exporter.constants import BLOCK_TYPES
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML

from .test_entities import Link


class URLDecorator:
    """
    Replace plain urls with actual hyperlinks.
    """
    SEARCH_RE = re.compile(r'(http://|https://|www\.)([a-zA-Z0-9\.\-%/\?&_=\+#:~!,\'\*\^$]+)')

    def __init__(self, new_window=False):
        self.new_window = new_window

    def replace(self, match, block_type):
        protocol = match.group(1)
        url = match.group(2)
        href = protocol + url
        if block_type == BLOCK_TYPES.CODE:
            return href

        text = cgi.escape(href)
        if href.startswith("www"):
            href = "http://" + href
        props = {'href': href}
        if self.new_window:
            props.update(target="_blank")

        return DOM.create_element('a', props, text)


class HashTagDecorator:
    """
    Wrap hash tags in spans with specific class.
    """
    SEARCH_RE = re.compile(r'#\w+')

    def replace(self, match, block_type):

        if block_type == BLOCK_TYPES.CODE:
            return match.group(0)

        return DOM.create_element(
            'span',
            {'class': 'hash_tag'}, match.group(0)
        )


class LineBreakDecorator:
    """
    Wrap hash tags in spans with specific class.
    """
    SEARCH_RE = re.compile(r'\n')

    def replace(self, match, block_type):

        if block_type == BLOCK_TYPES.CODE:
            return match.group(0)

        return DOM.create_element('br')


config = {
    'entity_decorators': {
        'LINK': Link()
    },
    'composite_decorators': [
        URLDecorator(),
        HashTagDecorator()
    ],
    'block_map': {
        BLOCK_TYPES.UNSTYLED: {'element': 'div'},
        BLOCK_TYPES.CODE: {'element': 'pre'}
    },
    'style_map': {
        'ITALIC': {'element': 'em'},
        'BOLD': {'element': 'strong'}
    }
}


class TestCompositeDecorator(unittest.TestCase):

    def setUp(self):
        self.exporter = HTML(config)
        self.maxDiff = None

    def test_render_with_entity_and_decorators(self):
        """
        The composite decorator should never render text in any entities.
        """
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
                {
                    'key': '34a12',
                    'text': '#check www.example.com',
                    'type': 'code-block',
                    'inlineStyleRanges': [],
                },
            ]
        }),
            '<div>search <a href="http://amazon.us">http://a.us</a> or '
            '<a href="https://yahoo.com">https://yahoo.com</a> or '
            '<a href="http://www.google.com">www.google.com</a> for '
            '<span class="hash_tag">#github</span> and '
            '<span class="hash_tag">#facebook</span></div>'
            '<pre>#check www.example.com</pre>')

    def test_render_with_multiple_decorators(self):
        """
        When multiple decorators match the same part of text,
        only the first one should perform the replacement.
        """
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'search http://www.google.com#world for the #world',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': [],
                },
            ]
        }),
            '<div>search <a href="http://www.google.com#world">'
            'http://www.google.com#world</a> for the '
            '<span class="hash_tag">#world</span></div>')
