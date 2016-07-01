from __future__ import absolute_import, unicode_literals

import unittest

from lxml import etree

from draftjs_exporter.entities.null import Null


class TestNull(unittest.TestCase):
    def setUp(self):
        self.null = Null()

    def test_init(self):
        self.assertIsInstance(self.null, Null)

    def test_call(self):
        elt = etree.Element('p')
        elt.text = 'Test text'
        self.assertEqual(self.null.call(elt).tag, 'p')
        self.assertEqual(self.null.call(elt).text, 'Test text')
