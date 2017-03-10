from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.options import Options


class StyleState:
    """
    Handles the creation of inline styles on elements.
    Receives inline_style commands, and generates the element's `style`
    attribute from those.
    """
    def __init__(self, style_map):
        self.styles = []
        self.style_map = style_map

    def apply(self, command):
        if command.name == 'start_inline_style':
            self.styles.append(command.data)
        elif command.name == 'stop_inline_style':
            self.styles.remove(command.data)

    def is_empty(self):
        return not self.styles

    def render_styles(self, text_node):
        if self.is_empty():
            node = text_node
        else:
            options = [Options.for_style(self.style_map, s) for s in self.styles]
            options.sort(key=lambda o: o.element)

            node = DOM.create_element(options[0].element, options[0].props)
            child = node

            # Nest the tags.
            for opt in options[1:]:
                new_child = DOM.create_element(opt.element, opt.props)
                DOM.append_child(child, new_child)
                child = new_child

            DOM.append_child(child, text_node)

        return node
