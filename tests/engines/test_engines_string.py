# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.engines.string import DOM_STRING


class TestDOM_STRING(unittest.TestCase):
    def test_create_tag(self):
        self.assertEqual(DOM_STRING.render_debug(DOM_STRING.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_create_tag_empty(self):
        self.assertEqual(DOM_STRING.render_debug(DOM_STRING.create_tag('p')), '<p></p>')

    def test_parse_html(self):
        with self.assertRaises(NotImplementedError):
            DOM_STRING.parse_html('<p><span>Test text</span></p>')

    def test_append_child(self):
        parent = DOM_STRING.create_tag('p')
        DOM_STRING.append_child(parent, DOM_STRING.create_tag('span', {}))
        self.assertEqual(DOM_STRING.render_debug(parent), '<p><span></span></p>')

    def test_render(self):
        self.assertEqual(DOM_STRING.render_debug(DOM_STRING.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_render_debug(self):
        self.assertEqual(DOM_STRING.render_debug(DOM_STRING.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')
