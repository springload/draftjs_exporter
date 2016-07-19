from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.entities.token import Token


class TestToken(unittest.TestCase):
    def setUp(self):
        self.token = Token()

    def test_init(self):
        self.assertIsInstance(self.token, Token)

    def test_render(self):
        self.assertEqual(self.token.render({}).tag, 'fragment')
        self.assertEqual(self.token.render({}).text, None)
