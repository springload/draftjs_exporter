from __future__ import absolute_import, unicode_literals

from lxml import etree


class Link():
    def call(self, parent_element, data):
        # TODO Use more than just url attribute https://github.com/sstur/draft-js-export-html/blob/master/src/stateToHTML.js#L30
        element = etree.SubElement(parent_element, 'a', attrib={'href': data.get('data', {}).get('url')})

        return element
