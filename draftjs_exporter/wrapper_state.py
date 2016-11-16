from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.error import ExporterException


class BlockException(ExporterException):
    pass


class WrapperState:
    """
    This class does the initial node building for the tree.
    It sets elements with the right tag, text content, and attributes.
    It adds a wrapper element around multiple elements, if required.
    """

    def __init__(self, block_map):
        self.block_map = block_map
        self.document = DOM.create_document_fragment()

        self.wrapper_stack = []

    def element_for(self, block):
        type_ = block.get('type', 'unstyled')
        depth = block.get('depth', 0)
        block_options = self.get_block_options(type_)

        # Make an element from the options specified in the block map.
        elt_options = self.map_element_options(block_options.get('element'))
        elt = DOM.create_element(elt_options[0], elt_options[1])

        parent = self.parent_for(block_options, depth)
        DOM.append_child(parent, elt)

        # At level 0, the element is added to the document.
        if depth == 0:
            DOM.append_child(self.document, parent)

        return elt

    def to_string(self):
        return DOM.render(self.document)

    def __str__(self):
        return '<WrapperState: %s>' % self.to_string()

    def set_wrapper(self, options=None, elt_options=None, depth=-1):
        if depth >= len(self.wrapper_stack):
            for d in range(len(self.wrapper_stack), depth + 1):
                wrapper_elt = self.create_wrapper_elt(options)
                new_wrapper = [wrapper_elt, d, options]

                wrapper_children = DOM.get_children(self.get_wrapper_elt())

                # Determine where to append the new wrapper.
                if len(wrapper_children) > 0:
                    wrapper_parent = wrapper_children[-1]
                else:
                    # If there is no content in the current wrapper, we need
                    # to add an intermediary node.
                    wrapper_parent = DOM.create_element(elt_options[0], elt_options[1])
                    DOM.append_child(self.get_wrapper_elt(), wrapper_parent)

                DOM.append_child(wrapper_parent, wrapper_elt)

                self.wrapper_stack.append(new_wrapper)
        else:
            wrapper_elt = self.create_wrapper_elt(options)
            new_wrapper = [wrapper_elt, depth, options]

            # Cut the stack to where it now stops, and add new wrapper.
            self.wrapper_stack = self.wrapper_stack[:depth] + [new_wrapper]

    def create_wrapper_elt(self, options):
        if options:
            wrapper_elt = DOM.create_element(options[0], options[1])
        else:
            wrapper_elt = DOM.create_document_fragment()

        return wrapper_elt

    def get_wrapper_elt(self, depth=-1):
        return self.wrapper_stack[depth][0] if len(self.wrapper_stack) > 0 else DOM.create_document_fragment()

    def get_wrapper_depth(self, depth=-1):
        return self.wrapper_stack[depth][1] if len(self.wrapper_stack) > 0 else -1

    def get_wrapper_options(self, depth=-1):
        return self.wrapper_stack[depth][2]

    def parent_for(self, block_options, depth):
        elt_options = self.map_element_options(block_options.get('element'))
        wrapper_options = block_options.get('wrapper', None)

        if wrapper_options:
            parent = self.get_wrapper(self.map_element_options(wrapper_options), elt_options, depth)
        else:
            parent = self.reset_wrapper_stack()

        return parent

    def reset_wrapper_stack(self):
        self.set_wrapper()
        return self.get_wrapper_elt()

    def map_element_options(self, opts):
        """
        Used for elements and wrappers. Supports the following options formats:
        'ul'
        ['ul']
        ['ul', {'className': 'bullet-list'}]
        """
        if isinstance(opts, list):
            tag = opts[0]
            attributes = opts[1] if len(opts) > 1 else {}
        else:
            tag = opts
            attributes = {}

        return [tag, attributes]

    def get_block_options(self, type_):
        block_options = self.block_map.get(type_)

        if block_options is None:
            raise BlockException('Block "%s" does not exist in block_map' % type_)

        return block_options

    def get_wrapper(self, wrapper_options, elt_options, depth):
        if depth > self.get_wrapper_depth() or wrapper_options != self.get_wrapper_options():
            self.set_wrapper(wrapper_options, elt_options, depth)

        # If depth is lower than the maximum, we need to cut the stack.
        if depth < self.get_wrapper_depth():
            self.wrapper_stack = self.wrapper_stack[:depth + 1]

        return self.get_wrapper_elt(depth)
