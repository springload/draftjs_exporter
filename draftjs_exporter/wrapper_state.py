from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.error import ExporterException


class BlockException(ExporterException):
    pass


class Options:
    """
    Facilitates querying configuration from the block_map.
    """

    @staticmethod
    def map(opts):
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

    @staticmethod
    def block(block_map, type_):
        block_options = block_map.get(type_)

        if block_options is None:
            raise BlockException('Block "%s" does not exist in block_map' % type_)

        return block_options


class WrapperStack:
    def __init__(self):
        self.stack = []


class WrapperState:
    """
    This class does the initial node building for the tree.
    It sets elements with the right tag, text content, and attributes.
    It adds a wrapper element around multiple elements, if required.
    """

    def __init__(self, block_map):
        self.block_map = block_map
        self.document = DOM.create_document_fragment()

        # Stack of nested wrapper elements. Each item has the following shape:
        # [elt (DOM node), depth level (int), options (list)]
        self.stack = []

    def element_for(self, block):
        type_ = block.get('type', 'unstyled')
        depth = block.get('depth', 0)
        block_options = Options.block(self.block_map, type_)

        # Make an element from the options specified in the block map.
        elt_options = Options.map(block_options.get('element'))
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
        if depth >= self.stack_length():
            for d in range(self.stack_length(), depth + 1):
                new_wrapper = self.create_wrapper(d, options)

                wrapper_children = DOM.get_children(self.get_top_wrapper().get('elt'))

                # Determine where to append the new wrapper.
                if len(wrapper_children) > 0:
                    wrapper_parent = wrapper_children[-1]
                else:
                    # If there is no content in the current wrapper, we need
                    # to add an intermediary node.
                    wrapper_parent = DOM.create_element(elt_options[0], elt_options[1])
                    DOM.append_child(self.get_top_wrapper().get('elt'), wrapper_parent)

                DOM.append_child(wrapper_parent, new_wrapper.get('elt'))

                self.stack.append(new_wrapper)
        else:
            new_wrapper = self.create_wrapper(depth, options)

            # Cut the stack to where it now stops, and add new wrapper.
            self.stack = self.stack[:depth] + [new_wrapper]

    def create_wrapper(self, depth, options):
        if options:
            elt = DOM.create_element(options[0], options[1])
        else:
            elt = DOM.create_document_fragment()

        return {
            'elt': elt,
            'depth': depth,
            'options': options,
        }

    def get_top_wrapper(self):
        if self.stack_length() > 0:
            wrapper = self.stack[-1]
        else:
            wrapper = self.create_wrapper(-1, None)

        return wrapper

    def parent_for(self, block_options, depth):
        elt_options = Options.map(block_options.get('element'))
        wrapper_options = block_options.get('wrapper', None)

        if wrapper_options:
            parent = self.get_wrapper(Options.map(wrapper_options), elt_options, depth)
        else:
            parent = self.reset_stack()

        return parent

    def get_wrapper(self, wrapper_options, elt_options, depth):
        if depth > self.get_top_wrapper().get('depth') or wrapper_options != self.get_top_wrapper().get('options'):
            self.set_wrapper(wrapper_options, elt_options, depth)

        # If depth is lower than the maximum, we need to cut the stack.
        if depth < self.get_top_wrapper().get('depth'):
            self.stack = self.stack[:depth + 1]

        return self.stack[depth].get('elt')

    def stack_length(self):
        return len(self.stack)

    def reset_stack(self):
        self.set_wrapper()
        return self.get_top_wrapper().get('elt')
