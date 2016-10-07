from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.wrapper_state import BlockException, WrapperState


class TestWrapperState(unittest.TestCase):
    def setUp(self):
        self.wrapper_state = WrapperState({
            'header-one': {'element': 'h1'},
            'unstyled': {'element': 'div'},
        })

    def test_init(self):
        self.assertIsInstance(self.wrapper_state, WrapperState)

    def test_element_for_text(self):
        self.assertEqual(DOM.get_text_content(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        })), None)

    def test_element_for_tag(self):
        self.assertEqual(DOM.get_tag_name(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        })), 'h1')

    def test_element_for_raises(self):
        with self.assertRaises(BlockException):
            self.wrapper_state.element_for({
                'key': '5s7g9',
                'text': 'Header',
                'type': 'header-two',
                'depth': 0,
                'inlineStyleRanges': [],
                'entityRanges': []
            })

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
        })

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
        })

        self.assertEqual(str(self.wrapper_state), '<WrapperState: <h1></h1>>')

    def test_map_element_options_full(self):
        self.assertEqual(self.wrapper_state.map_element_options([
            'ul',
            {'className': 'bullet-list'},
        ]), [
            'ul',
            {'className': 'bullet-list'},
        ])

    def test_map_element_options_half(self):
        self.assertEqual(self.wrapper_state.map_element_options([
            'ul',
        ]), [
            'ul',
            {},
        ])

    def test_map_element_options_simplest(self):
        self.assertEqual(self.wrapper_state.map_element_options('ul'), [
            'ul',
            {},
        ])
