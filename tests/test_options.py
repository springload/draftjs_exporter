from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.options import ConfigException, Options


class TestOptions(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Options('li')), '<Options li None None None>')

    def test_eq(self):
        self.assertEqual(Options('li'), Options('li'))

    def test_not_eq(self):
        self.assertNotEqual(Options('li'), Options('p'))

    def test_for_block_full(self):
        block_map = {'unordered-list-item': 'li'}
        self.assertEqual(Options.for_block(block_map, 'unordered-list-item'), Options('li'))

    def test_for_block_half(self):
        block_map = {'unordered-list-item': 'li'}
        self.assertEqual(Options.for_block(block_map, 'unordered-list-item'), Options('li'))

    def test_for_block_simplest(self):
        block_map = {'unordered-list-item': 'li'}
        self.assertEqual(Options.for_block(block_map, 'unordered-list-item'), Options('li'))

    def test_for_block_raises_missing_type(self):
        block_map = {'header-one': 'h1'}
        with self.assertRaises(ConfigException):
            Options.for_block(block_map, 'header-two')

    def test_for_block_raises_missing_element(self):
        block_map = {'header-one': {}}
        with self.assertRaises(ConfigException):
            Options.for_block(block_map, 'header-one')

    def test_for_block_raises_wrong_format(self):
        block_map = {'header-one': []}
        with self.assertRaises(ConfigException):
            Options.for_block(block_map, 'header-one')
