from __future__ import absolute_import, unicode_literals

import unittest

from lxml import etree

from draftjs_exporter.command import Command
from draftjs_exporter.style_state import StyleState

style_map = {
    'ITALIC': {'fontStyle': 'italic'},
    'BOLD': {'fontStyle': 'bold'},
    'HIGHLIGHT': {'fontStyle': 'bold', 'textDecoration': 'underline'},
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
        self.assertEqual(self.style_state.get_style_value(), 'font-style: italic;')

    def test_get_style_value_multiple(self):
        self.style_state.apply(Command('start_inline_style', 0, 'HIGHLIGHT'))
        self.assertEqual(self.style_state.get_style_value(), 'font-style: bold;text-decoration: underline;')

    def test_element_attributes_empty(self):
        self.assertEqual(self.style_state.element_attributes(), {})

    def test_element_attributes_single(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.element_attributes(), {'style': 'font-style: italic;'})

    def test_add_node_unstyled(self):
        self.assertEqual(self.style_state.add_node(etree.Element('p'), 'Test text').tag, 'textnode')
        self.assertEqual(self.style_state.add_node(etree.Element('p'), 'Test text').text, 'Test text')

    def test_add_node_styled(self):
        self.style_state.apply(Command('start_inline_style', 0, 'ITALIC'))
        self.assertEqual(self.style_state.add_node(etree.Element('p'), 'Test text').tag, 'span')
        self.assertEqual(self.style_state.add_node(etree.Element('p'), 'Test text').get('style'), 'font-style: italic;')
        self.assertEqual(self.style_state.add_node(etree.Element('p'), 'Test text').text, 'Test text')
        self.style_state.apply(Command('stop_inline_style', 9, 'ITALIC'))
