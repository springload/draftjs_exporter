from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.wrapper_state import WrapperState


class TestWrapperState(unittest.TestCase):
    def setUp(self):
        self.wrapper_state = WrapperState({
            'header-one': 'h1',
            'unstyled': 'div',
            'atomic': lambda props: props['children'],
            'ignore': None,
        })

    def test_init(self):
        self.assertIsInstance(self.wrapper_state, WrapperState)

    def test_element_for_simple_content(self):
        self.assertEqual(DOM.render(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }, 'Header')), '<h1>Header</h1>')

    def test_element_for_element_content(self):
        self.assertEqual(DOM.render(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Paragraph',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }, DOM.create_element('strong', {}, 'Paragraph'))), '<div><strong>Paragraph</strong></div>')

    def test_element_for_dismiss_content(self):
        self.assertEqual(DOM.render(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Paragraph',
            'type': 'ignore',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }, DOM.create_element('img', {'src': '/example.png'}))), '')

    def test_element_for_no_block(self):
        self.assertEqual(DOM.render(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Paragraph',
            'type': 'atomic',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }, DOM.create_element('img', {'src': '/example.png'}))), '<img src="/example.png"/>')

    def test_to_string_empty(self):
        self.assertEqual(self.wrapper_state.to_string(), '')

    def test_to_string_elts(self):
        self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }, '')

        self.assertEqual(self.wrapper_state.to_string(), '<h1></h1>')

    def test_str_empty(self):
        self.assertEqual(str(self.wrapper_state), '<WrapperState: >')

    def test_str_elts(self):
        self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }, '')

        self.assertEqual(str(self.wrapper_state), '<WrapperState: <h1></h1>>')
