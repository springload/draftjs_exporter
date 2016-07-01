from __future__ import absolute_import, unicode_literals

from lxml import etree


class Link():
    attributes = ['url', 'rel', 'target', 'title']

    # TODO To unit test.
    def is_valid_attribute(self, key):
        valid_data_attr = (key.startswith('data-') and key.replace('data-', '') and key.replace('data-', '').islower())
        return key in Link.attributes or valid_data_attr

    def call(self, parent_element, options):
        data = options.get('data', {})
        attrib = {}
        for key in data:
            # TODO How much do we need to whitelist / blacklist attributes?
            if data[key] and self.is_valid_attribute(key):
                attr = key if key != 'url' else 'href'
                attrib[attr] = str(data[key])

        # TODO attributes will be in an unpredictable sort order. Use elt.set(attr, val) instead?
        return etree.SubElement(parent_element, 'a', attrib=attrib)
