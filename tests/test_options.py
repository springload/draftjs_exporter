from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.error import ConfigException
from draftjs_exporter.options import Options


class TestOptions(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(Options('unordered-list-item', 'li')), '<Options unordered-list-item li {} None None>')

    def test_eq(self):
        self.assertEqual(Options('unordered-list-item', 'li'), Options('unordered-list-item', 'li'))

    def test_not_eq(self):
        self.assertNotEqual(Options('unordered-list-item', 'li'), Options('unordered-list-item', 'p'))

    def test_create_full(self):
        self.assertEqual(Options.create({'unordered-list-item': 'li'}, 'unordered-list-item', 'fallback'), Options('unordered-list-item', 'li'))

    def test_create_half(self):
        self.assertEqual(Options.create({'unordered-list-item': 'li'}, 'unordered-list-item', 'fallback'), Options('unordered-list-item', 'li'))

    def test_create_simplest(self):
        self.assertEqual(Options.create({'unordered-list-item': 'li'}, 'unordered-list-item', 'fallback'), Options('unordered-list-item', 'li'))

    def test_create_uses_fallback(self):
        self.assertEqual(Options.create({'header-one': 'h1', 'fallback': 'div'}, 'header-two', 'fallback'), Options('header-two', 'div'))

    def test_create_raises_missing_type(self):
        with self.assertRaises(ConfigException):
            Options.create({'header-one': 'h1'}, 'header-two', 'fallback')

    def test_create_raises_missing_element(self):
        with self.assertRaises(ConfigException):
            Options.create({'header-one': {}}, 'header-one', 'fallback')

    def test_map_works(self):
        self.assertEqual(Options.map({
            'BOLD': 'strong',
            'HIGHLIGHT': {
                'element': 'strong',
                'props': {'style': {'textDecoration': 'underline'}},
            },
        }, 'FALLBACK'), {
            'BOLD': Options('BOLD', 'strong'),
            'HIGHLIGHT': Options('HIGHLIGHT', 'strong', props={'style': {'textDecoration': 'underline'}}),
        })

    def test_get_works(self):
        self.assertEqual(Options.get(Options.map({
            'BOLD': 'strong',
            'HIGHLIGHT': {
                'element': 'strong',
                'props': {'style': {'textDecoration': 'underline'}},
            },
        }, 'FALLBACK'), 'BOLD', 'FALLBACK'), Options('BOLD', 'strong'))

    def test_get_raises_exception(self):
        with self.assertRaises(ConfigException):
            self.assertEqual(Options.get(Options.map({
                'BOLD': 'strong',
            }, 'FALLBACK'), 'ITALIC', 'FALLBACK'), Options('BOLD', 'strong'))

    def test_get_uses_fallback(self):
        self.assertEqual(Options.get(Options.map({
            'BOLD': 'strong',
            'FALLBACK': 'span',
        }, 'FALLBACK'), 'ITALIC', 'FALLBACK'), Options('FALLBACK', 'span'))
