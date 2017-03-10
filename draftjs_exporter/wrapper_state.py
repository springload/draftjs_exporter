from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.error import ExporterException


class BlockException(ExporterException):
    pass


class Options:
    """
    Facilitates querying configuration from the block_map.
    """
    def __init__(self, element, props=None, wrapper=None, wrapper_props=None):
        self.element = element
        self.props = props
        self.wrapper = wrapper
        self.wrapper_props = wrapper_props

    def __str__(self):
        return '<Options {0} {1} {2} {3}>'.format(self.element, self.props, self.wrapper, self.wrapper_props)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def for_block(block_map, type_):
        if type_ not in block_map:
            raise BlockException('Block "%s" does not exist in block_map' % type_)

        block = block_map.get(type_)

        if isinstance(block, dict):
            if 'element' not in block:
                raise BlockException('Block "%s" does not define an element' % type_)

            opts = Options(**block)
        else:
            opts = Options(block)

        return opts


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
            wrapper = Wrapper(-1)

        return wrapper

    def tail(self):
        return self.get(0)


class Wrapper:
    """
    A wrapper is an element that wraps other nodes. It gets created
    when the depth of a block is different than 0, so the DOM elements
    have the appropriate amount of nesting.
    """
    def __init__(self, depth, elt=None, props=None):
        self.depth = depth
        self.type = elt
        self.elt = DOM.create_element(elt, props)
        self.props = props

    def is_different(self, depth, elt, props):
        return depth > self.depth or elt != self.type or props != self.props



class WrapperState:
    """
    This class does the initial node building for the tree.
    It sets elements with the right tag, text content, and props.
    It adds a wrapper element around elements, if required.
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
        elt = DOM.create_element(options.element, options.props)

        parent = self.parent_for(options, depth, elt)

        # At level 0, the element is added to the document.
        if depth == 0:
            DOM.append_child(self.document, parent)

        return elt

    def parent_for(self, options, depth, elt):
        if options.wrapper:
            parent = self.get_wrapper_elt(options, depth)
            DOM.append_child(parent, elt)
        else:
            # Reset the stack if there is no wrapper.
            head = self.stack.head()
            if self.stack.length() > 0 and head.depth != -1 and head.props is not None:
                self.stack.slice(-1)
                self.stack.append(Wrapper(-1, None))
            parent = elt

        return parent

    def get_wrapper_elt(self, options, depth):
        head = self.stack.head()
        if head.is_different(depth, options.wrapper, options.wrapper_props):
            self.update_stack(options, depth)

        # If depth is lower than the maximum, we cut the stack.
        if depth < head.depth:
            self.stack.slice(depth + 1)

        return self.stack.get(depth).elt

    def update_stack(self, options, depth):
        if depth >= self.stack.length():
            # If the depth is gte the stack length, we need more wrappers.
            depth_levels = range(self.stack.length(), depth + 1)

            for level in depth_levels:
                new_wrapper = Wrapper(level, options.wrapper, options.wrapper_props)

                wrapper_children = DOM.get_children(self.stack.head().elt)

                # Determine where to append the new wrapper.
                if len(wrapper_children) == 0:
                    # If there is no content in the current wrapper, we need
                    # to add an intermediary node.
                    wrapper_parent = DOM.create_element(options.element, options.props)
                    DOM.append_child(self.stack.head().elt, wrapper_parent)
                else:
                    # Otherwise we can append at the end of the last child.
                    wrapper_parent = wrapper_children[-1]

                DOM.append_child(wrapper_parent, new_wrapper.elt)

                self.stack.append(new_wrapper)
        else:
            # Cut the stack to where it now stops, and add new wrapper.
            self.stack.slice(depth)
            self.stack.append(Wrapper(depth, options.wrapper, options.wrapper_props))
