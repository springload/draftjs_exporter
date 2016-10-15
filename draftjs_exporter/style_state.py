from __future__ import absolute_import, unicode_literals

import re

from draftjs_exporter.dom import DOM

# TODO Extract to utils
# https://gist.github.com/yahyaKacem/8170675
_first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camelToDash(camelCasedStr):
    sub2 = _first_cap_re.sub(r'\1-\2', camelCasedStr)
    dashed_case_str = _all_cap_re.sub(r'\1-\2', sub2).lower()
    return dashed_case_str.replace('--', '-')


class StyleState():
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

    # TODO To unit test.
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
                    rules.append('{0}: {1};'.format(camelToDash(prop), css_style[prop]))

        return ''.join(sorted(rules))

    def add_node(self, element, text):
        if self.is_unstyled():
            child = DOM.create_text_node(text)
            DOM.append_child(element, child)
        else:
            tags = self.get_style_tags()
            child = element

            # Nest the tags.
            # Set the text and style attribute (if any) on the deepest node.
            for tag in tags:
                new_child = DOM.create_element(tag)
                DOM.append_child(child, new_child)
                child = new_child

            style_value = self.get_style_value()
            if style_value:
                DOM.set_attribute(child, 'style', style_value)

            DOM.set_text_content(child, text)

        return child
