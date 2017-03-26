from __future__ import absolute_import, unicode_literals

import inspect
import re

from lxml import etree, html

NSMAP = {
    'xlink': 'http://www.w3.org/1999/xlink',
}

# Python 2/3 unicode compatibility hack.
# See http://stackoverflow.com/questions/6812031/how-to-make-unicode-string-with-python3
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    def unicode(s):
        return str(s)

# https://gist.github.com/yahyaKacem/8170675
_first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def camel_to_dash(camel_cased_str):
    sub2 = _first_cap_re.sub(r'\1-\2', camel_cased_str)
    dashed_case_str = _all_cap_re.sub(r'\1-\2', sub2).lower()
    return dashed_case_str.replace('--', '-')


class DOM_LXML(object):
    """
    Wrapper around our HTML building library to facilitate changes.
    """
    @staticmethod
    def create_tag(type_, attr=None):
        nsmap = None

        if attr:
            # Never render children attribute on a raw tag.
            attr.pop('children', None)

            # Never render block attribute on a raw tag.
            attr.pop('block', None)

            if 'xlink:href' in attr:
                attr['{%s}href' % NSMAP['xlink']] = attr.pop('xlink:href')
                nsmap = NSMAP

            if 'style' in attr and isinstance(attr['style'], dict):
                rules = ['{0}: {1};'.format(camel_to_dash(s), attr['style'][s]) for s in attr['style'].keys()]
                attr['style'] = ''.join(sorted(rules))

            # Map props from React/Draft.js to HTML lingo.
            if 'className' in attr:
                attr['class'] = attr.pop('className')

            attributes = {}
            for key in attr:
                if attr[key] is False:
                    attr[key] = 'false'

                if attr[key] is True:
                    attr[key] = 'true'

                if attr[key] is not None:
                    attributes[key] = unicode(attr[key])

            attr = attributes

        return etree.Element(type_, attrib=attr, nsmap=nsmap)

    @staticmethod
    def create_element(type_=None, props=None, *children):
        """
        Signature inspired by React.createElement.
        createElement(
          string/ReactClass type,
          [object props],
          [children ...]
        )
        https://facebook.github.io/react/docs/top-level-api.html#react.createelement
        """
        if props is None:
            props = {}

        if not type_:
            return DOM_LXML.create_document_fragment()
        else:
            if len(children) and isinstance(children[0], (list, tuple)):
                children = children[0]

            if inspect.isclass(type_):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_().render(props)
            elif callable(getattr(type_, 'render', None)):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_.render(props)
            elif callable(type_):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_(props)
            else:
                elt = DOM_LXML.create_tag(type_, props)

                for child in children:
                    if child not in (None, ''):
                        if hasattr(child, 'tag'):
                            elt.append(child)
                        else:
                            elt_text = DOM_LXML.get_text_content(elt) or ''
                            elt_text += child
                            DOM_LXML.set_text_content(elt, elt_text)

        return elt

    @staticmethod
    def create_document_fragment():
        return DOM_LXML.create_tag('fragment')

    @staticmethod
    def parse_html(markup):
        return html.fromstring(markup)

    @staticmethod
    def camel_to_dash(camel_cased_str):
        return camel_to_dash(camel_cased_str)

    @staticmethod
    def append_child(elt, child):
        if hasattr(child, 'tag'):
            elt.append(child)
        else:
            c = DOM_LXML.create_document_fragment()
            DOM_LXML.set_text_content(c, child)
            elt.append(c)

    @staticmethod
    def get_text_content(elt):
        return ''.join(elt.itertext())

    @staticmethod
    def set_text_content(elt, text):
        elt.text = text

    @staticmethod
    def get_children(elt):
        return elt.getchildren()

    @staticmethod
    def render(elt):
        """
        Removes the fragments that should not have HTML tags. Caveat of lxml.
        Dirty, but quite easy to understand.
        """
        return re.sub(r'(</?(fragment)>|xmlns:xlink="http://www.w3.org/1999/xlink" )', '', etree.tostring(elt, method='html', encoding='unicode'))

    @staticmethod
    def render_debug(elt):
        return re.sub(r'(xmlns:xlink="http://www.w3.org/1999/xlink" )', '', etree.tostring(elt, method='html', encoding='unicode'))

    @staticmethod
    def pretty_print(markup):
        """
        Convenience method.
        Pretty print the element, removing the top-level node that lxml needs.
        """
        return re.sub(r'</?doc>', '',
                      etree.tostring(
                          html.fromstring('<doc>%s</doc>' % markup),
                          encoding='unicode',
                          pretty_print=True))
