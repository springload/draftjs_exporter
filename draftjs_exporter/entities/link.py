from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM


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
