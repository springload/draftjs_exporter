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
        node = text_node
        if not self.is_empty():
            # Nest the tags.
            for s in sorted(self.styles, reverse=True):
                opt = Options.for_style(self.style_map, s)
                node = DOM.create_element(opt.element, opt.props, node)

        return node
