from __future__ import absolute_import, unicode_literals

import re
import unittest

from draftjs_exporter.composite_decorators import render_decorators
from draftjs_exporter.constants import BLOCK_TYPES
from draftjs_exporter.dom import DOM


class Linkify:
    """
    Wrap plain URLs with link tags.
    See http://pythex.org/?regex=(http%3A%2F%2F%7Chttps%3A%2F%2F%7Cwww%5C.)(%5Ba-zA-Z0-9%5C.%5C-%25%2F%5C%3F%26_%3D%5C%2B%23%3A~!%2C%5C%27%5C*%5C%5E%24%5D%2B)&test_string=search%20http%3A%2F%2Fa.us%20or%20https%3A%2F%2Fyahoo.com%20or%20www.google.com%20for%20%23github%20and%20%23facebook&ignorecase=0&multiline=0&dotall=0&verbose=0
    for an example.
    """
    SEARCH_RE = re.compile(r'(http://|https://|www\.)([a-zA-Z0-9\.\-%/\?&_=\+#:~!,\'\*\^$]+)')

    def __init__(self, use_new_window=False):
        self.use_new_window = use_new_window

    def render(self, props):
        match = props.get('match')
        protocol = match.group(1)
        url = match.group(2)
        href = protocol + url

        if props['block_type'] == BLOCK_TYPES.CODE:
            return href

        link_props = {
            'href': href,
        }

        if self.use_new_window:
            link_props['target'] = '_blank'
            link_props['rel'] = 'noreferrer noopener'

        if href.startswith('www'):
            link_props['href'] = 'http://' + href

        return DOM.create_element('a', link_props, href)


class Hashtag:
    """
    Wrap hashtags in spans with a specific class.
    """
    SEARCH_RE = re.compile(r'#\w+')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block_type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('span', {'class': 'hashtag'}, props['children'])


class BR:
    """
    Replace line breaks (\n) with br tags.
    """
    SEARCH_RE = re.compile(r'\n')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block_type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('br')


class TestLinkify(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Linkify(), Linkify)

    def test_render(self):
        match = next(Linkify.SEARCH_RE.finditer('test https://www.example.com'))

        self.assertEqual(DOM.render(DOM.create_element(Linkify, {
            'block_type': BLOCK_TYPES.UNSTYLED,
            'match': match,
            'children': match.group(0),
        })), '<a href="https://www.example.com">https://www.example.com</a>')

    def test_render_www(self):
        match = next(Linkify.SEARCH_RE.finditer('test www.example.com'))

        self.assertEqual(DOM.render(DOM.create_element(Linkify, {
            'block_type': BLOCK_TYPES.UNSTYLED,
            'match': match,
            'children': match.group(0),
        })), '<a href="http://www.example.com">www.example.com</a>')

    def test_render_code_block(self):
        match = next(Linkify.SEARCH_RE.finditer('test https://www.example.com'))

        self.assertEqual(DOM.create_element(Linkify, {
            'block_type': BLOCK_TYPES.CODE,
            'match': match,
            'children': match.group(0),
        }), match.group(0))

    def test_render_new_window(self):
        match = next(Linkify.SEARCH_RE.finditer('test https://www.example.com'))

        self.assertEqual(DOM.render(DOM.create_element(Linkify(use_new_window=True), {
            'block_type': BLOCK_TYPES.UNSTYLED,
            'match': match,
            'children': match.group(0),
        })), '<a href="https://www.example.com" rel="noreferrer noopener" target="_blank">https://www.example.com</a>')


class TestHashtag(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Hashtag(), Hashtag)

    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element(Hashtag, {
            'block_type': BLOCK_TYPES.UNSTYLED,
            'children': '#hashtagtest',
        })), '<span class="hashtag">#hashtagtest</span>')

    def test_render_code_block(self):
        self.assertEqual(DOM.render(DOM.create_element(Hashtag, {
            'block_type': BLOCK_TYPES.CODE,
            'children': '#hashtagtest',
        })), '#hashtagtest')


class TestBR(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(BR(), BR)

    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element(BR, {
            'block_type': BLOCK_TYPES.UNSTYLED,
            'children': '\n',
        })), '<br/>')

    def test_render_code_block(self):
        self.assertEqual(DOM.create_element(BR, {
            'block_type': BLOCK_TYPES.CODE,
            'children': '\n',
        }), '\n')


class TestCompositeDecorators(unittest.TestCase):
    def test_render_decorators_empty(self):
        self.assertEqual(DOM.render(render_decorators([], 'test https://www.example.com#hash #hashtagtest', BLOCK_TYPES.UNSTYLED)), 'test https://www.example.com#hash #hashtagtest')

    def test_render_decorators_single(self):
        self.assertEqual(DOM.render(render_decorators([Linkify()], 'test https://www.example.com#hash #hashtagtest', BLOCK_TYPES.UNSTYLED)), 'test <a href="https://www.example.com#hash">https://www.example.com#hash</a> #hashtagtest')

    def test_render_decorators_conflicting_order_one(self):
        self.assertEqual(DOM.render(render_decorators([Linkify(), Hashtag()], 'test https://www.example.com#hash #hashtagtest', BLOCK_TYPES.UNSTYLED)), 'test <a href="https://www.example.com#hash">https://www.example.com#hash</a> <span class="hashtag">#hashtagtest</span>')

    def test_render_decorators_conflicting_order_two(self):
        self.assertEqual(DOM.render(render_decorators([Hashtag(), Linkify()], 'test https://www.example.com#hash #hashtagtest', BLOCK_TYPES.UNSTYLED)), 'test https://www.example.com<span class="hashtag">#hash</span> <span class="hashtag">#hashtagtest</span>')
