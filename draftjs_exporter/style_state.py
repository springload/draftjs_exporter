import re

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
        if (command.name == 'start_inline_style'):
            self.styles.append(command.data)
        elif (command.name == 'stop_inline_style'):
            self.styles.remove(command.data)

    def is_unstyled(self):
        return not self.styles

    def element_attributes(self):
        return {} if len(self.styles) == 0 else {
            'style': self.get_style_value()
        }

    def get_style_value(self):
        rules = []

        for style in self.styles:
            css_style = self.style_map.get(style, {})
            for prop in css_style.keys():
                rules.append('{0}: {1};'.format(camelToDash(prop), css_style[prop]))

        return ''.join(sorted(rules))
