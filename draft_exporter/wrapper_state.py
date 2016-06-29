from lxml import etree


class WrapperState():
    """
    This class does the initial node building for the tree.
    It sets elements with the right tag, text content, and attributes.
    It adds a wrapper element around multiple elements, if required.
    """

    def __init__(self, block_map):
        self.block_map = block_map
        # TODO lxml does not have the notion of a document fragment.
        # Or does it? How do we deal with this?
        self.fragment = etree.Element('fragment')
        self.document = etree.Element('root')

        # Default wrapper element is a fragment, does not have options.
        self.wrapper = [self.fragment, []]

    def element_for(self, block):
        type = block.get('type', 'unstyled')
        # print(type, self.block_options(type))

        elt = etree.Element(self.block_options(type))

        # TODO To remove
        elt.text = block.get('text')

        parent = self.parent_for(type)
        parent.append(elt)

        self.document.append(parent)

        return elt

    def to_string(self):
        # Even dirtier but easier to understand.
        return etree.tostring(self.document).replace('<root/>', '').replace('<root>', '').replace('</root>', '').replace('<fragment>', '').replace('</fragment>', '').replace('<textnode>', '').replace('</textnode>', '')

    # def to_string(self):
    #     # Semi-dirty trick to get rid of fragment tags.
    #     for fragment in self.document.iterfind('.//fragment'):
    #         for child in fragment.getchildren():
    #             fragment.getparent().append(child)
    #         fragment.getparent().remove(fragment)

    #     # Dirty trick to get rid of the top-level "root" element
    #     return ''.join([etree.tostring(elt) for elt in list(self.document)])

    def __str__(self):
        return '<WrapperState: %s>' % self.to_string()

    def set_wrapper(self, element, options=[]):
        self.wrapper = [element, options]

    def get_wrapper_elt(self):
        return self.wrapper[0]

    def get_wrapper_options(self):
        return self.wrapper[1]

    # TODO Refactor to remove multi-returns
    def parent_for(self, type):
        parent = None
        options = self.block_map.get(type)

        if 'wrapper' in options:
            parent = self.create_wrapper(options.get('wrapper'))
        else:
            parent = self.reset_wrapper()

        return parent

    def reset_wrapper(self):
        self.set_wrapper(self.fragment)
        return self.get_wrapper_elt()

    def map_options(self, name, attributes={}):
        """
        Map attributes/options from Draft.js to lxml lingo.
        """
        attributes['class'] = attributes.get('className', None)
        attributes.pop('className', None)

        return [name, attributes]

    def block_options(self, type):
        return self.block_map.get(type).get('element')

    def create_wrapper(self, options):
        new_options = self.map_options(options[0], options[1])

        # TODO Check object equality in Python
        if new_options != self.get_wrapper_options():
            wrapper = etree.Element(options[0], attrib=options[1])
            # self.reset_wrapper().append(wrapper)
            self.set_wrapper(wrapper, options)

        return self.get_wrapper_elt()
