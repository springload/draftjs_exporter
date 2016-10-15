from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.entities import Image, Link, Null


class TestNull(unittest.TestCase):
    def setUp(self):
        self.null = Null()

    def test_init(self):
        self.assertIsInstance(self.null, Null)

    def test_render(self):
        self.assertEqual(DOM.get_tag_name(self.null.render({})), 'fragment')
        self.assertEqual(DOM.get_text_content(self.null.render({})), None)


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


class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Link()

    def test_init(self):
        self.assertIsInstance(self.link, Link)

    def test_render(self):
        link = self.link.render({
            'data': {
                'url': 'http://example.com',
            }
        })
        self.assertEqual(DOM.get_tag_name(link), 'a')
        self.assertEqual(DOM.get_text_content(link), None)
        self.assertEqual(link.get('href'), 'http://example.com')

    def test_render_invalid(self):
        link = self.link.render({
            'data': {
                'url': 'http://example.com',
                'disabled': 'true',
            }
        })
        self.assertEqual(link.get('disabled'), None)
