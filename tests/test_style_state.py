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

    def test_is_unstyled_default(self):
        self.assertEqual(self.style_state.is_unstyled(), True)

    def test_is_unstyled_styled(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.is_unstyled(), False)

    def test_get_style_value_empty(self):
        self.assertEqual(self.style_state.get_style_value(), '')

    def test_get_style_value_single(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.get_style_value(), '')

    def test_get_style_value_multiple(self):
        self.style_state.apply(Command('start_inline_style', 0, 'HIGHLIGHT'))
        self.assertEqual(self.style_state.get_style_value(), 'text-decoration: underline;')

    def test_add_node_unstyled(self):
        self.assertEqual(DOM.get_tag_name(self.style_state.add_node(DOM.create_element('p'), 'Test text')), 'textnode')
        self.assertEqual(DOM.get_text_content(self.style_state.add_node(DOM.create_element('p'), 'Test text')), 'Test text')

    def test_add_node_unicode(self):
        self.assertEqual(DOM.get_text_content(self.style_state.add_node(DOM.create_element('p'), '🍺')), '🍺')

    def test_add_node_styled(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(DOM.get_tag_name(self.style_state.add_node(DOM.create_element('p'), 'Test text')), 'em')
        self.assertEqual(self.style_state.add_node(DOM.create_element('p'), 'Test text').get('style'), None)
        self.assertEqual(DOM.get_text_content(self.style_state.add_node(DOM.create_element('p'), 'Test text')), 'Test text')
        self.style_state.apply(Command('stop_inline_style', 9, 'ITALIC'))
