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
            DOM_STRING.parse_html('<p>Test text</p>')

    def test_append_child(self):
        parent = DOM_STRING.create_tag('p')
        DOM_STRING.append_child(parent, DOM_STRING.create_tag('span', {}))
        self.assertEqual(DOM_STRING.render_debug(parent), '<p><span></span></p>')

    def test_render_attrs(self):
        self.assertEqual(DOM_STRING.render_attrs({
            'src': 'src.png',
            'alt': 'img\'s alt',
            'class': 'intro',
        }), ' alt="img&#x27;s alt" class="intro" src="src.png"')


    def test_render_children(self):
        self.assertEqual(DOM_STRING.render_children([
            'render children',
            DOM_STRING.create_tag('p', {'class': 'intro'}),
            'test test',
        ]), 'render children<p class="intro"></p>test test')

    def test_render(self):
        self.assertEqual(DOM_STRING.render_debug(DOM_STRING.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_render_debug(self):
        self.assertEqual(DOM_STRING.render_debug(DOM_STRING.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')
