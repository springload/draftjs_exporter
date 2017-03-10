from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM


def Null(props):
    return DOM.create_element()


def HR(props):
    return DOM.create_element('hr')


class Link:
    def render(self, props):
        data = props.get('data', {})
        attributes = {}
        for key in data:
            attr = key if key != 'url' else 'href'
            attributes[attr] = data[key]

        return DOM.create_element('a', attributes, props['children'])


class Image:
    def render(self, props):
        data = props.get('data', {})

        return DOM.create_element('img', {
            'src': data.get('src'),
            'width': data.get('width'),
            'height': data.get('height'),
            'alt': data.get('alt'),
        })


class Icon:
    def __init__(self, icon_class='icon'):
        self.icon_class = icon_class

    def render(self, props):
        href = '#icon-%s' % props.get('name', '')
        return DOM.create_element('svg', {'class': self.icon_class}, DOM.create_element('use', {'xlink:href': href}))


class Button:
    def render(self, props):
        data = props.get('data', {})
        href = data.get('href', '#')
        icon = data.get('icon', None)
        text = data.get('text', '')

        return DOM.create_element(
            'a',
            {'class': 'icon-text' if icon else None, 'href': href},
            DOM.create_element(Icon, {'name': icon}) if icon else None,
            DOM.create_element('span', {'class': 'icon-text__text'}, text) if icon else text
        )


class TestNull(unittest.TestCase):
    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element(Null)), '')


class TestIcon(unittest.TestCase):
    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element(Icon, {'name': 'rocket'})), '<svg class="icon"><use xlink:href="#icon-rocket"></use></svg>')

    def test_render_configured(self):
        self.assertEqual(DOM.render(DOM.create_element(Icon(icon_class='i'), {'name': 'rocket'})), '<svg class="i"><use xlink:href="#icon-rocket"></use></svg>')


class TestImage(unittest.TestCase):
    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element(Image, {
            'data': {
                'src': 'http://example.com/example.png',
                'width': 320,
                'height': 580,
            }
        })), '<img height="580" src="http://example.com/example.png" width="320"/>')


class TestLink(unittest.TestCase):
    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element(Link, {
            'data': {
                'url': 'http://example.com',
            },
        }, 'wow')), '<a href="http://example.com">wow</a>')


class TestButton(unittest.TestCase):
    def test_render_with_icon(self):
        self.assertEqual(DOM.render(DOM.create_element(Button, {
            'data': {
                'href': 'http://example.com',
                'icon': 'rocket',
                'text': 'Launch',
            }
        })), '<a class="icon-text" href="http://example.com"><svg class="icon"><use xlink:href="#icon-rocket"></use></svg><span class="icon-text__text">Launch</span></a>')

    def test_render_without_icon(self):
        self.assertEqual(DOM.render(DOM.create_element(Button, {
            'data': {
                'href': 'http://example.com',
                'text': 'Launch',
            }
        })), '<a href="http://example.com">Launch</a>')
