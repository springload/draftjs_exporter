from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES


class TestConstants(unittest.TestCase):
    def test_block_types(self):
        self.assertIsInstance(BLOCK_TYPES, object)
        self.assertEqual(BLOCK_TYPES.UNSTYLED, 'unstyled')

    def test_entity_types(self):
        self.assertIsInstance(ENTITY_TYPES, object)
        self.assertEqual(ENTITY_TYPES.LINK, 'LINK')

    def test_inline_styles(self):
        self.assertIsInstance(INLINE_STYLES, object)
        self.assertEqual(INLINE_STYLES.BOLD, 'BOLD')
