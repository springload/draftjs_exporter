from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM


class Null:
    def render(self, props):
        return DOM.create_element()


class Icon:
    def render(self, props):
        href = 'icon-%s' % props.get('name', '')
        return DOM.create_element('svg', {'class': 'icon'}, DOM.create_element('use', {'xlink:href': href}))


class Image:
    def render(self, props):
        data = props.get('data', {})

        return DOM.create_element('img', {
            'src': data.get('src'),
            'width': data.get('width'),
            'height': data.get('height'),
            'alt': data.get('alt'),
        })


class Link:
    def render(self, props):
        data = props.get('data', {})
        attributes = {}
        for key in data:
            attr = key if key != 'url' else 'href'
            attributes[attr] = data[key]

        return DOM.create_element('a', attributes, props['children'])


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
