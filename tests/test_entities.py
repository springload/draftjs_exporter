from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.entities import Button, Icon, Image, Link, Null


class TestNull(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Null(), Null)

    def test_render(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_element(Null, {})), 'fragment')
        self.assertEqual(DOM.get_text_content(DOM.create_element(Null, {})), None)


class TestIcon(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Icon(), Icon)

    def test_render(self):
        icon = DOM.create_element(Icon, {
            'name': 'rocket',
        })
        self.assertEqual(DOM.get_tag_name(icon), 'svg')
        self.assertEqual(DOM.get_text_content(icon), None)
        self.assertEqual(DOM.get_class_list(icon), ['icon'])
        self.assertEqual(DOM.render(icon), '<svg class="icon"><use xlink:href="icon-rocket"></use></svg>')


class TestImage(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Image(), Image)

    def test_render(self):
        image = DOM.create_element(Image, {
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
    def test_init(self):
        self.assertIsInstance(Link(), Link)

    def test_render(self):
        link = DOM.create_element(Link, {
            'data': {
                'url': 'http://example.com',
            }
        })
        self.assertEqual(DOM.get_tag_name(link), 'a')
        self.assertEqual(DOM.get_text_content(link), None)
        self.assertEqual(link.get('href'), 'http://example.com')

    def test_render_invalid(self):
        link = DOM.create_element(Link, {
            'data': {
                'url': 'http://example.com',
                'disabled': 'true',
            }
        })
        self.assertEqual(link.get('disabled'), None)


class TestButton(unittest.TestCase):
    def test_init(self):
        self.assertIsInstance(Button(), Button)

    def test_render_with_icon(self):
        button = DOM.create_element(Button, {
            'data': {
                'href': 'http://example.com',
                'icon': 'rocket',
                'text': 'Launch',
            }
        })
        self.assertEqual(DOM.get_tag_name(button), 'a')
        self.assertEqual(DOM.get_text_content(button), None)
        self.assertEqual(button.get('href'), 'http://example.com')
        self.assertEqual(DOM.get_class_list(button), ['icon-text'])
        self.assertEqual(DOM.render(button), '<a class="icon-text" href="http://example.com"><svg class="icon"><use xlink:href="icon-rocket"></use></svg><span class="icon-text__text">Launch</span></a>')

    def test_render_without_icon(self):
        button = DOM.create_element(Button, {
            'data': {
                'href': 'http://example.com',
                'text': 'Launch',
            }
        })
        self.assertEqual(DOM.get_tag_name(button), 'a')
        self.assertEqual(DOM.get_text_content(button), 'Launch')
        self.assertEqual(button.get('href'), 'http://example.com')
        self.assertEqual(DOM.get_class_list(button), [])
        self.assertEqual(DOM.render(button), '<a href="http://example.com">Launch</a>')
