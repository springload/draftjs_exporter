from __future__ import absolute_import, unicode_literals

import unittest

from lxml import etree

from draftjs_exporter.entities.link import Link


class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Link()

    def test_init(self):
        self.assertIsInstance(self.link, Link)

    def test_call(self):
        elt = etree.Element('p')
        link = self.link.call(elt, {
            'data': {
                'url': 'http://example.com',
            }
        })
        self.assertEqual(link.tag, 'a')
        self.assertEqual(link.text, None)
        self.assertEqual(link.get('href'), 'http://example.com')
        self.assertEqual(link.getparent().tag, 'p')
