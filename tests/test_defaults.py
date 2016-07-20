from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP


class TestDefaults(unittest.TestCase):
    def test_default_block_map(self):
        self.assertIsInstance(BLOCK_MAP, object)

    def test_default_style_map(self):
        self.assertIsInstance(STYLE_MAP, object)
