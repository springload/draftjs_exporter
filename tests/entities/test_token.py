from __future__ import absolute_import, unicode_literals

import unittest

from lxml import etree

from draftjs_exporter.entities.token import Token


class TestToken(unittest.TestCase):
    def setUp(self):
        self.token = Token()

    def test_init(self):
        self.assertIsInstance(self.token, Token)

    def test_call(self):
        elt = etree.Element('p')
        elt.text = 'Test text'
        self.assertEqual(self.token.call(elt, {}).tag, 'p')
        self.assertEqual(self.token.call(elt, {}).text, 'Test text')
