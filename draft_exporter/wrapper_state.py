from lxml.html import builder as E
from lxml import html, etree


class WrapperState():
    def __init__(self, block_map):
        self.block_map = block_map
        self.document = E.DIV()

    def element_for(self, block):
        type = block.get('type', 'unstyled')
        # print(type, self.block_options(type))

        elt = etree.Element(self.block_options(type))
        elt.text = block.get('text')

        self.document.append(elt)

    def to_string(self):
        return etree.tostring(self.document, pretty_print=True)

    def to_browser(self):
        return html.open_in_browser(self.document)

    def __str__(self):
        return self.to_string()

    def set_wrapper(self, element, options={}):
        pass

    def parent_for(self, type):
        pass

    def reset_wrapper(self):
        pass

    def block_options(self, type):
        return self.block_map.get(type).get('element')
