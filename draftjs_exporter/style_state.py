from __future__ import absolute_import, unicode_literals

import re

from draftjs_exporter.dom import DOM

# TODO Extract to utils
# https://gist.github.com/yahyaKacem/8170675
_first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_dash(camel_cased_str):
    sub2 = _first_cap_re.sub(r'\1-\2', camel_cased_str)
    dashed_case_str = _all_cap_re.sub(r'\1-\2', sub2).lower()
    return dashed_case_str.replace('--', '-')


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

    def is_unstyled(self):
        return not self.styles

    def get_style_tags(self):
        tags = []

        for style in self.styles:
            config = self.style_map.get(style, {})
            tags.append(config.get('element', 'span'))

        return sorted(list(set(tags)))

    def get_style_value(self):
        rules = []

        for style in self.styles:
            css_style = self.style_map.get(style, {})
            for prop in css_style.keys():
                if prop != 'element':
                    rules.append('{0}: {1};'.format(camel_to_dash(prop), css_style[prop]))

        return ''.join(sorted(rules))

    def create_node(self, text):
        if self.is_unstyled():
            node = DOM.create_text_node(text)
        else:
            tags = self.get_style_tags()
            node = DOM.create_element(tags[0])
            child = node

            # Nest the tags.
            # Set the text and style attribute (if any) on the deepest node.
            for tag in tags[1:]:
                new_child = DOM.create_element(tag)
                DOM.append_child(child, new_child)
                child = new_child

            style_value = self.get_style_value()
            if style_value:
                DOM.set_attribute(child, 'style', style_value)

            DOM.set_text_content(child, text)

        return node
