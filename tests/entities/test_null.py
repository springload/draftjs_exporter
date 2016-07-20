from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.entities.null import Null


class TestNull(unittest.TestCase):
    def setUp(self):
        self.null = Null()

    def test_init(self):
        self.assertIsInstance(self.null, Null)

    def test_render(self):
        self.assertEqual(self.null.render({}).tag, 'fragment')
        self.assertEqual(self.null.render({}).text, None)
