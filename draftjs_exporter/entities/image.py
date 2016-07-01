from __future__ import absolute_import, unicode_literals

from lxml import etree


class Image():
    def call(self, parent_element, data):
        # TODO Use more than just src attribute https://github.com/sstur/draft-js-export-html/blob/master/src/stateToHTML.js#L30
        element = etree.SubElement(parent_element, 'img', attrib={'src': data.get('data', {}).get('src')})

        return element
