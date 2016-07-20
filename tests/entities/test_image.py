from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.entities.image import Image


class TestImage(unittest.TestCase):
    def setUp(self):
        self.image = Image()

    def test_init(self):
        self.assertIsInstance(self.image, Image)

    def test_render(self):
        image = self.image.render({
            'data': {
                'src': 'http://example.com/example.png',
                'width': 320,
                'height': 580,
            }
        })
        self.assertEqual(DOM.get_tag_name(image), 'img')
        self.assertEqual(DOM.get_text_content(image), None)
        self.assertEqual(image.get('src'), 'http://example.com/example.png')
