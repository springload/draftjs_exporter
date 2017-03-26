from __future__ import absolute_import, unicode_literals

import inspect
import re

from bs4 import BeautifulSoup
from .dom_lxml import DOM_LXML

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


def Soup(raw_str):
    """
    Wrapper around BeautifulSoup to keep the code DRY.
    """
    return BeautifulSoup(raw_str, 'html5lib')


# Cache empty soup so we can create tags in isolation without the performance overhead.
soup = Soup('')


def create_tag(type_, attr=None):
    """
    Wrapper around our HTML building library to facilitate changes.
    """
    if not attr:
        attr = {}
    else:
        # Never render children attribute on a raw tag.
        attr.pop('children', None)

        # Never render block attribute on a raw tag.
        attr.pop('block', None)

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

    return soup.new_tag(type_, **attr)


def create_document_fragment():
    return create_tag('fragment')


def get_text_content(elt):
    return elt.string


def set_text_content(elt, text):
    elt.append(text)


class DOM_BS(object):
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
        if not type_:
            elt = create_document_fragment()
        else:
            if props is None:
                props = {}

            # Class component.
            if inspect.isclass(type_):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_().render(props)
            # Object instance component.
            elif callable(getattr(type_, 'render', None)):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_.render(props)
            # Functional component.
            elif callable(type_):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_(props)
            else:
                elt = create_tag(type_, props)

                for child in children:
                    if child:
                        if hasattr(child, 'tag'):
                            DOM_BS.append_child(elt, child)
                        else:
                            set_text_content(elt, get_text_content(elt) + child if get_text_content(elt) else child)

        return elt

    @staticmethod
    def parse_html(markup):
        return Soup(markup)

    @staticmethod
    def camel_to_dash(camel_cased_str):
        return camel_to_dash(camel_cased_str)

    @staticmethod
    def append_child(elt, child):
        elt.append(child)

    @staticmethod
    def get_children(elt):
        return list(elt.children)

    @staticmethod
    def render(elt):
        """
        Removes the fragments that should not have HTML tags. Left-over from
        when this library relied on the lxml HTTP parser. There might be a
        better way to do this.
        Dirty, but quite easy to understand.
        """
        return re.sub(r'</?(fragment|body|html|head)>', '', unicode(elt)).strip()

    @staticmethod
    def render_debug(elt):
        return re.sub(r'</?(body|html|head)>', '', unicode(elt)).strip()


DOM = DOM_BS
