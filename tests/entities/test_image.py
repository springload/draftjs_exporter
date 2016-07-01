from __future__ import absolute_import, unicode_literals

import unittest

from lxml import etree

from draftjs_exporter.entities.image import Image


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = Image()

    def test_init(self):
        self.assertIsInstance(self.image, Image)

    def test_call(self):
        elt = etree.Element('p')
        image = self.image.call(elt, {
            'data': {
                'src': 'http://example.com/example.png',
            }
        })
        self.assertEqual(image.tag, 'img')
        self.assertEqual(image.text, None)
        self.assertEqual(image.get('src'), 'http://example.com/example.png')
        self.assertEqual(image.getparent().tag, 'p')
