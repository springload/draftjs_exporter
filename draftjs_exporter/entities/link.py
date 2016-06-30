from lxml import etree


class Link():
    def call(self, parent_element, data):
        element = etree.SubElement(parent_element, 'a', attrib={'href': data.get('data', {}).get('url')})

        return element
