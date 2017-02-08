# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.command import Command
from draftjs_exporter.dom import DOM
from draftjs_exporter.style_state import StyleState

style_map = {
    'ITALIC': {'element': 'em'},
    'BOLD': {'element': 'strong'},
    'HIGHLIGHT': {'element': 'strong', 'textDecoration': 'underline'},
}


class TestStyleState(unittest.TestCase):
    def setUp(self):
        self.style_state = StyleState(style_map)

    def test_init(self):
        self.assertIsInstance(self.style_state, StyleState)

    def test_apply_start_inline_style(self):
        self.assertEqual(self.style_state.styles, [])
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.styles, ['ITALIC'])

    def test_apply_stop_inline_style(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.style_state.apply(Command('stop_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.styles, [])

    def test_is_empty_default(self):
        self.assertEqual(self.style_state.is_empty(), True)

    def test_is_empty_styled(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.is_empty(), False)

    def test_get_style_value_empty(self):
        self.assertEqual(self.style_state.get_style_value(), '')

    def test_get_style_value_single(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.get_style_value(), '')

    def test_get_style_value_multiple(self):
        self.style_state.apply(Command('start_inline_style', 0, 'HIGHLIGHT'))
        self.assertEqual(self.style_state.get_style_value(), 'text-decoration: underline;')

    def test_render_styles_unstyled(self):
        self.assertEqual(DOM.get_tag_name(self.style_state.render_styles(DOM.create_text_node('Test text'))), 'textnode')
        self.assertEqual(DOM.get_text_content(self.style_state.render_styles(DOM.create_text_node('Test text'))), 'Test text')

    def test_render_styles_unicode(self):
        self.assertEqual(DOM.get_text_content(self.style_state.render_styles(DOM.create_text_node('🍺'))), '🍺')

    def test_render_styles_styled(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(DOM.get_tag_name(self.style_state.render_styles(DOM.create_text_node('Test text'))), 'em')
        self.assertEqual(self.style_state.render_styles(DOM.create_text_node('Test text')).get('style'), None)
        self.assertEqual(DOM.get_text_content(self.style_state.render_styles(DOM.create_text_node('Test text'))), 'Test text')
        self.style_state.apply(Command('stop_inline_style', 9, 'ITALIC'))

    def test_render_styles_styled_multiple(self):
        self.style_state.apply(Command('start_inline_style', 0, 'BOLD'))
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.get_style_tags(), ['em', 'strong'])
        self.assertEqual(DOM.get_tag_name(self.style_state.render_styles(DOM.create_text_node('Test text'))), 'em')
        self.assertEqual(DOM.get_tag_name(DOM.get_children(self.style_state.render_styles(DOM.create_text_node('Test text')))[0]), 'strong')
