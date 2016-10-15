from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM


class Null():
    def render(self, props):
        return DOM.create_element()


class Icon():
    def render(self, props):
        href = 'icon-%s' % props.get('name', '')
        return DOM.create_element('svg', {'class': 'icon'}, DOM.create_element('use', {'xlink:href': href}))


class Image():
    def render(self, props):
        data = props.get('data', {})

        return DOM.create_element('img', {
            'src': data.get('src'),
            'width': data.get('width'),
            'height': data.get('height'),
            'alt': data.get('alt'),
        })


class Link():
    attributes = ['url', 'rel', 'target', 'title']

    @staticmethod
    def is_valid_attribute(key):
        # TODO How much do we need to whitelist / blacklist attributes?
        valid_data_attr = (key.startswith('data-') and key.replace('data-', '') and key.replace('data-', '').islower())
        return key in Link.attributes or valid_data_attr

    def render(self, props):
        data = props.get('data', {})
        # TODO attributes will be in an unpredictable sort order. Use elt.set(attr, val) instead?
        # Use from collections import OrderedDict?
        attributes = {}
        for key in data:
            if data[key] and Link.is_valid_attribute(key):
                attr = key if key != 'url' else 'href'
                attributes[attr] = data[key]

        return DOM.create_element('a', attributes)


class Button():
    def render(self, props):
        data = props.get('data', {})
        href = data.get('href', '#')
        icon = data.get('icon', None)
        text = data.get('text', '')

        return DOM.create_element('a', {'class': 'icon-text' if icon else None, 'href': href}, DOM.create_element(Icon, {'name': icon}) if icon else None, DOM.create_element('span', {'class': 'icon-text__text'}, text) if icon else text)
