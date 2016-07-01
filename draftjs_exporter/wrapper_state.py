from __future__ import absolute_import, unicode_literals

import re

from lxml import etree

from draftjs_exporter.error import ExporterException


class BlockException(ExporterException):
    pass


class WrapperState():
    """
    This class does the initial node building for the tree.
    It sets elements with the right tag, text content, and attributes.
    It adds a wrapper element around multiple elements, if required.
    """

    def __init__(self, block_map):
        self.block_map = block_map
        self.document = etree.Element('root')

        # Default wrapper element is a fragment, does not have options.
        self.wrapper = [etree.Element('fragment'), []]

    def element_for(self, block):
        type = block.get('type', 'unstyled')
        elt = etree.Element(self.get_block_tag(type))

        parent = self.parent_for(type)
        parent.append(elt)

        self.document.append(parent)

        return elt

    def to_string(self):
        # Even dirtier but easier to understand.
        return re.sub(r'</?(root|fragment|textnode)>', '', etree.tostring(self.document, method='html').decode('utf-8'))

    def __str__(self):
        return '<WrapperState: %s>' % self.to_string()

    def set_wrapper(self, element, options=[]):
        self.wrapper = [element, options]

    def get_wrapper_elt(self):
        return self.wrapper[0]

    def get_wrapper_options(self):
        return self.wrapper[1]

    def parent_for(self, type):
        parent = None
        options = self.block_map.get(type)

        if 'wrapper' in options:
            parent = self.create_wrapper(options.get('wrapper'))
        else:
            parent = self.reset_wrapper()

        return parent

    def reset_wrapper(self):
        self.set_wrapper(etree.Element('fragment'))
        return self.get_wrapper_elt()

    def map_options(self, name, attributes={}):
        """
        Map attributes/options from Draft.js to lxml lingo.
        """
        if 'className' in attributes:
            attributes['class'] = attributes.get('className')
            attributes.pop('className', None)

        return [name, attributes]

    def get_block_tag(self, type):
        options = self.block_map.get(type)

        # TODO To test
        if options is None:
            raise BlockException('Block "%s" does not exist in block_map' % type)

        return options.get('element')

    def create_wrapper(self, options):
        new_options = self.map_options(options[0], options[1])

        if new_options != self.get_wrapper_options():
            wrapper = etree.Element(options[0], attrib=options[1])
            self.set_wrapper(wrapper, options)

        return self.get_wrapper_elt()
