from lxml.html import builder as E
from lxml import html


class WrapperState():
    def __init__(self, block_map):
        self.block_map = block_map
        self.fragment = E.HTML(E.BODY())

    def element_for(self, block):
        type = block.get('type', 'unstyled')
        print(type)
        print(self.block_options(type))

        self.document.create_element(self.block_options(type))

    def to_string(self):
        return html.tostring(self.fragment, pretty_print=True)

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
