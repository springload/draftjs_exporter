from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.wrapper_state import BlockException, WrapperState

block_map = {
    'header-one': {'element': 'h1'},
    'unstyled': {'element': 'div'}
}


class TestWrapperState(unittest.TestCase):
    def setUp(self):
        self.wrapper_state = WrapperState(block_map)

    def test_init(self):
        self.assertIsInstance(self.wrapper_state, WrapperState)

    def test_element_for_text(self):
        self.assertEqual(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }).text, None)

    def test_element_for_tag(self):
        self.assertEqual(self.wrapper_state.element_for({
            'key': '5s7g9',
            'text': 'Header',
            'type': 'header-one',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        }).tag, 'h1')

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

    # def test_set_wrapper(self):
    #     # self.assertEqual(self.wrapper_state.set_wrapper(element, options=[]), '')
    #     pass

    # def test_get_wrapper_elt(self):
    #     # self.assertEqual(self.wrapper_state.get_wrapper_elt( '')
    #     pass

    # def test_get_wrapper_options(self):
    #     # self.assertEqual(self.wrapper_state.get_wrapper_options( '')
    #     pass

    # def test_parent_for(self):
    #     # self.assertEqual(self.wrapper_state.parent_for(type), '')
    #     pass

    # def test_reset_wrapper(self):
    #     # self.assertEqual(self.wrapper_state.reset_wrapper( '')
    #     pass

    # def test_map_options(self):
    #     # self.assertEqual(self.wrapper_state.map_options(name, attributes={}), '')
    #     pass

    # def test_block_options(self):
    #     # self.assertEqual(self.wrapper_state.block_options(type), '')
    #     pass

    # def test_create_wrapper(self):
    #     # self.assertEqual(self.wrapper_state.create_wrapper(options), '')
    #     pass
