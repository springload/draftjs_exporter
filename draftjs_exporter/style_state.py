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

    def render_styles(self, decorated_node, block, blocks):
        node = decorated_node
        if not self.is_empty():
            # Nest the tags.
            for style in sorted(self.styles, reverse=True):
                opt = Options.for_style(self.style_map, style)
                props = dict(opt.props)
                props['block'] = block
                props['blocks'] = blocks
                props['inline_style_range'] = {
                    'style': style,
                }
                node = DOM.create_element(opt.element, props, node)

        return node
