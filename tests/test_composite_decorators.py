from __future__ import absolute_import, unicode_literals

import cgi
import re
import unittest

from draftjs_exporter.constants import BLOCK_TYPES
from draftjs_exporter.dom import DOM


class Linkify:
    """
    Wrap plain URLs with link tags.
    See http://pythex.org/?regex=(http%3A%2F%2F%7Chttps%3A%2F%2F%7Cwww%5C.)(%5Ba-zA-Z0-9%5C.%5C-%25%2F%5C%3F%26_%3D%5C%2B%23%3A~!%2C%5C%27%5C*%5C%5E%24%5D%2B)&test_string=search%20http%3A%2F%2Fa.us%20or%20https%3A%2F%2Fyahoo.com%20or%20www.google.com%20for%20%23github%20and%20%23facebook&ignorecase=0&multiline=0&dotall=0&verbose=0
    for an example.
    """
    SEARCH_RE = re.compile(r'(http://|https://|www\.)([a-zA-Z0-9\.\-%/\?&_=\+#:~!,\'\*\^$]+)')

    def __init__(self, new_window=False):
        self.new_window = new_window

    def render(self, props):
        match = props.get('match')
        block_type = props.get('block_type')
        protocol = match.group(1)
        url = match.group(2)
        href = protocol + url

        if block_type == BLOCK_TYPES.CODE:
            return href

        text = cgi.escape(href)
        if href.startswith('www'):
            href = 'http://' + href

        props = {
            'href': href,
        }

        if self.new_window:
            props.update(target="_blank", rel="noreferrer noopener")

        return DOM.create_element('a', props, text)


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

# class TestLinkify(unittest.TestCase):
#     def test_init(self):
#         self.assertIsInstance(Linkify(), Linkify)

#     def test_render(self):
#         self.assertEqual(DOM.get_tag_name(DOM.create_element(Linkify, {})), 'fragment')
#         self.assertEqual(DOM.get_text_content(DOM.create_element(Linkify, {})), None)


class TestCompositeDecorators(unittest.TestCase):

    def setUp(self):
        pass
