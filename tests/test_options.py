from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.options import ConfigException, Options


class TestOptions(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Options('li')), '<Options li {} None None>')

    def test_eq(self):
        self.assertEqual(Options('li'), Options('li'))

    def test_not_eq(self):
        self.assertNotEqual(Options('li'), Options('p'))

    def test_for_block_full(self):
        self.assertEqual(Options.for_block({'unordered-list-item': 'li'}, 'unordered-list-item'), Options('li'))

    def test_for_block_half(self):
        self.assertEqual(Options.for_block({'unordered-list-item': 'li'}, 'unordered-list-item'), Options('li'))

    def test_for_block_simplest(self):
        self.assertEqual(Options.for_block({'unordered-list-item': 'li'}, 'unordered-list-item'), Options('li'))

    def test_for_block_raises_missing_type(self):
        with self.assertRaises(ConfigException):
            Options.for_block({'header-one': 'h1'}, 'header-two')

    def test_for_block_raises_missing_element(self):
        with self.assertRaises(ConfigException):
            Options.for_block({'header-one': {}}, 'header-one')

    def test_for_block_raises_wrong_format(self):
        with self.assertRaises(ConfigException):
            Options.for_block({'header-one': []}, 'header-one')

    def test_for_style_full(self):
        self.assertEqual(Options.for_style({'ITALIC': 'em'}, 'ITALIC'), Options('em'))

    def test_for_style_half(self):
        self.assertEqual(Options.for_style({'ITALIC': 'em'}, 'ITALIC'), Options('em'))

    def test_for_style_simplest(self):
        self.assertEqual(Options.for_style({'ITALIC': 'em'}, 'ITALIC'), Options('em'))

    def test_for_style_raises_missing_type(self):
        with self.assertRaises(ConfigException):
            Options.for_style({'BOLD': 'strong'}, 'CODE')

    def test_for_style_raises_missing_element(self):
        with self.assertRaises(ConfigException):
            Options.for_style({'BOLD': {}}, 'BOLD')
