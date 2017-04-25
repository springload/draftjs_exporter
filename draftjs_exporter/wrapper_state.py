from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.options import Options


class WrapperStack:
    """
    Stack data structure for element wrappers.
    The bottom of the stack contains the elements closest to the page body.
    The top of the stack contains the most nested nodes.
    """
    def __init__(self):
        self.stack = []

    def __str__(self):
        return str(self.stack)

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
            wrapper = self.stack[-1]
        else:
            wrapper = Wrapper(-1)

        return wrapper

    def tail(self):
        return self.stack[0]


class Wrapper:
    """
    A wrapper is an element that wraps other nodes. It gets created
    when the depth of a block is different than 0, so the DOM elements
    have the appropriate amount of nesting.
    """
    def __init__(self, depth, options=None):
        self.depth = depth
        self.last_child = None

        if options:
            self.type = options.wrapper
            self.props = options.wrapper_props

            wrapper_props = dict(self.props) if self.props else {}
            wrapper_props['block'] = {
                'type': options.type,
                'depth': depth,
            }

            self.elt = DOM.create_element(self.type, wrapper_props)
        else:
            self.type = None
            self.props = None
            self.elt = DOM.create_element()


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
        self.stack = WrapperStack()

    def __str__(self):
        return '<WrapperState: %s>' % self.stack

    def element_for(self, block, block_content):
        type_ = block['type']
        depth = block['depth']
        data = block.get('data', {})
        options = Options.for_block(self.block_map, type_)
        props = dict(options.props)
        props['block'] = {
            'type': type_,
            'depth': depth,
            'data': data,
        }

        # Make an element from the options specified in the block map.
        elt = DOM.create_element(options.element, props, block_content)

        parent = self.parent_for(options, depth, elt)

        return parent

    def parent_for(self, options, depth, elt):
        if options.wrapper:
            parent = self.get_wrapper_elt(options, depth)
            DOM.append_child(parent, elt)
            self.stack.stack[-1].last_child = elt
        else:
            # Reset the stack if there is no wrapper.
            self.stack = WrapperStack()
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
                new_wrapper = Wrapper(level, options)

                # Determine where to append the new wrapper.
                if self.stack.head().last_child is None:
                    # If there is no content in the current wrapper, we need
                    # to add an intermediary node.
                    props = dict(options.props)
                    props['block'] = {
                        'type': options.type,
                        'depth': depth,
                        'data': {},
                    }
                    wrapper_parent = DOM.create_element(options.element, props)
                    DOM.append_child(self.stack.head().elt, wrapper_parent)
                else:
                    # Otherwise we can append at the end of the last child.
                    wrapper_parent = self.stack.head().last_child

                DOM.append_child(wrapper_parent, new_wrapper.elt)

                self.stack.append(new_wrapper)
        else:
            # Cut the stack to where it now stops, and add new wrapper.
            self.stack.slice(depth)
            self.stack.append(Wrapper(depth, options))
