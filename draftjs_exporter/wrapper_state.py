from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.error import ExporterException


class BlockException(ExporterException):
    pass


class Options:
    """
    Facilitates querying configuration from the block_map.
    """
    def __init__(self, element_options, wrapper_options):
        self.element = Options.map(element_options)
        self.wrapper = Options.map(wrapper_options) if wrapper_options else None

    @staticmethod
    def map(opts):
        """
        Supports the following options formats:
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

    @staticmethod
    def for_block(block_map, type_):
        block_options = block_map.get(type_)

        if block_options is None:
            raise BlockException('Block "%s" does not exist in block_map' % type_)

        return Options(block_options.get('element'), block_options.get('wrapper'))


class WrapperStack:
    """
    Stack data structure for element wrappers.
    The bottom of the stack contains the elements closest to the page body.
    The top of the stack contains the most nested nodes.
    """
    def __init__(self):
        self.stack = []

    def length(self):
        return len(self.stack)

    def append(self, wrapper):
        return self.stack.append(wrapper)

    def get(self, index):
        return self.stack[index]

    def slice(self, length):
        self.stack = self.stack[:length]

    def head(self):
        if self.length() > 0:
            wrapper = self.get(-1)
        else:
            wrapper = Wrapper(-1, None)

        return wrapper

    def tail(self):
        return self.get(0)


class Wrapper:
    """
    A wrapper is an element that wraps other nodes. It gets created
    when the depth of a block is different than 0, so the DOM elements
    have the appropriate amount of nesting.
    """
    def __init__(self, depth, options):
        if options:
            self.elt = DOM.create_element(options[0], options[1])
        else:
            self.elt = DOM.create_document_fragment()

        self.depth = depth
        self.options = options


class WrapperState:
    """
    This class does the initial node building for the tree.
    It sets elements with the right tag, text content, and attributes.
    It adds a wrapper element around multiple elements, if required.
    """

    def __init__(self, block_map):
        self.block_map = block_map
        self.document = DOM.create_document_fragment()

        self.stack = WrapperStack()

    def __str__(self):
        return '<WrapperState: %s>' % self.to_string()

    def to_string(self):
        return DOM.render(self.document)

    def clean_up(self):
        """
        Special method to handle a rare corner case: if there is no block
        at depth 0, we need to add the wrapper that contains the whole
        tree to the document.
        """
        document_length = len(DOM.get_children(self.document))

        if document_length == 0 and self.stack.length() != 0:
            DOM.append_child(self.document, self.stack.tail().elt)

    def element_for(self, block):
        type_ = block.get('type', 'unstyled')
        depth = block.get('depth', 0)
        options = Options.for_block(self.block_map, type_)

        # Make an element from the options specified in the block map.
        elt = DOM.create_element(options.element[0], options.element[1])

        parent = self.parent_for(options, depth)
        DOM.append_child(parent, elt)

        # At level 0, the element is added to the document.
        if depth == 0:
            DOM.append_child(self.document, parent)

        return elt

    def parent_for(self, options, depth):
        if options.wrapper:
            parent = self.get_wrapper_elt(options, depth)
        else:
            # Reset the stack if there is no wrapper.
            self.stack.slice(-1)
            self.stack.append(Wrapper(-1, None))
            parent = self.stack.head().elt

        return parent

    def get_wrapper_elt(self, options, depth):
        if depth > self.stack.head().depth or options.wrapper != self.stack.head().options:
            self.update_stack(options, depth)

        # If depth is lower than the maximum, we cut the stack.
        if depth < self.stack.head().depth:
            self.stack.slice(depth + 1)

        return self.stack.get(depth).elt

    def update_stack(self, options, depth):
        if depth >= self.stack.length():
            # If the depth is gte the stack length, we need more wrappers.
            depth_levels = range(self.stack.length(), depth + 1)

            for level in depth_levels:
                new_wrapper = Wrapper(level, options.wrapper)

                wrapper_children = DOM.get_children(self.stack.head().elt)

                # Determine where to append the new wrapper.
                if len(wrapper_children) == 0:
                    # If there is no content in the current wrapper, we need
                    # to add an intermediary node.
                    wrapper_parent = DOM.create_element(options.element[0], options.element[1])
                    DOM.append_child(self.stack.head().elt, wrapper_parent)
                else:
                    # Otherwise we can append at the end of the last child.
                    wrapper_parent = wrapper_children[-1]

                DOM.append_child(wrapper_parent, new_wrapper.elt)

                self.stack.append(new_wrapper)
        else:
            # Cut the stack to where it now stops, and add new wrapper.
            self.stack.slice(depth)
            self.stack.append(Wrapper(depth, options.wrapper))
