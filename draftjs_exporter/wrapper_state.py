from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
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
        self.document = DOM.create_document_fragment()

        self.wrapper_stack = [
            # Default wrapper element is a fragment, does not have options.
            [DOM.create_document_fragment(), 0, []],
        ]

    def element_for(self, block):
        type = block.get('type', 'unstyled')
        depth = block.get('depth', 0)
        tag = self.get_block_tag(type)
        elt = DOM.create_element(tag)

        parent = self.parent_for(type, depth)
        DOM.append_child(parent, elt)

        # At level 0, the element is added to the document.
        if (depth == 0):
            DOM.append_child(self.document, parent)

        return elt

    def to_string(self):
        return DOM.render(self.document)

    def __str__(self):
        return '<WrapperState: %s>' % self.to_string()

    def set_wrapper(self, element, depth=0, options=[]):
        new_wrapper = [element, depth, options]

        if depth >= len(self.wrapper_stack):
            DOM.append_child(DOM.get_children(self.get_wrapper_elt())[-1], element)

            self.wrapper_stack.append(new_wrapper)
        else:
            # Cut the stack to where it now stops, and add new wrapper.
            self.wrapper_stack = self.wrapper_stack[:depth] + [new_wrapper]

    def get_wrapper_elt(self, depth=-1):
        return self.wrapper_stack[depth][0]

    def get_wrapper_depth(self, depth=-1):
        return self.wrapper_stack[depth][1]

    def get_wrapper_options(self, depth=-1):
        return self.wrapper_stack[depth][2]

    def parent_for(self, type, depth):
        parent = None
        options = self.block_map.get(type)

        if 'wrapper' in options:
            parent = self.create_wrapper(options.get('wrapper'), depth)
        else:
            parent = self.reset_wrapper_stack()

        return parent

    def reset_wrapper_stack(self):
        self.set_wrapper(DOM.create_document_fragment())
        return self.get_wrapper_elt()

    def map_options(self, tag, attributes={}):
        return [tag, attributes]

    def get_block_tag(self, type):
        options = self.block_map.get(type)

        if options is None:
            raise BlockException('Block "%s" does not exist in block_map' % type)

        return options.get('element')

    def create_wrapper(self, options, depth):
        new_options = self.map_options(options[0], options[1])

        if depth > self.get_wrapper_depth() or new_options != self.get_wrapper_options():
            wrapper = DOM.create_element(options[0], options[1])
            self.set_wrapper(wrapper, depth, options)

        return self.get_wrapper_elt(depth)
