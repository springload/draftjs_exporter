from __future__ import absolute_import, unicode_literals

import inspect
import re

from bs4 import BeautifulSoup

# Python 2/3 unicode compatibility hack.
# See http://stackoverflow.com/questions/6812031/how-to-make-unicode-string-with-python3
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)


def Soup(raw_str):
    """
    Wrapper around BeautifulSoup to keep the code DRY.
    """
    return BeautifulSoup(raw_str, 'html5lib')


# Cache empty soup so we can create tags in isolation without the performance overhead.
soup = Soup('')


class DOM(object):
    """
    Wrapper around our HTML building library to facilitate changes.
    """
    @staticmethod
    def create_tag(type_, attributes=None):
        if attributes is None:
            attributes = {}

        return soup.new_tag(type_, **attributes)

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
            elt = DOM.create_document_fragment()
        else:
            attributes = {}

            # Map props from React/Draft.js to HTML lingo.
            if 'className' in props:
                props['class'] = props.pop('className')

            for key in props:
                prop = props[key]
                # Filter None values.
                if prop is not None:
                    attributes[key] = prop

            if inspect.isclass(type_):
                elt = type_().render(attributes)
            elif callable(getattr(type_, 'render', None)):
                elt = type_.render(attributes)
            elif callable(type_):
                elt = type_(attributes)
            else:
                elt = DOM.create_tag(type_, attributes)

        for child in children:
            if child:
                if hasattr(child, 'tag'):
                    DOM.append_child(elt, child)
                else:
                    DOM.set_text_content(elt, DOM.get_text_content(elt) + child if DOM.get_text_content(elt) else child)

        return elt

    @staticmethod
    def create_document_fragment():
        return DOM.create_tag('fragment')

    @staticmethod
    def create_text_node(text):
        elt = DOM.create_tag('textnode')
        DOM.set_text_content(elt, text)
        return elt

    @staticmethod
    def parse_html(markup):
        return Soup(markup)

    @staticmethod
    def append_child(elt, child):
        elt.append(child)

    @staticmethod
    def set_attribute(elt, attr, value):
        elt[attr] = value

    @staticmethod
    def get_tag_name(elt):
        return elt.name

    @staticmethod
    def get_class_list(elt):
        return elt.get('class', [])

    @staticmethod
    def get_text_content(elt):
        return elt.string

    @staticmethod
    def set_text_content(elt, text):
        elt.string = text

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
        return re.sub(r'</?(fragment|textnode|body|html|head)>', '', unicode(elt)).strip()

    @staticmethod
    def pretty_print(markup):
        """
        Convenience method.
        Pretty print the element, removing the top-level nodes that html5lib adds.
        """
        return re.sub(r'</?(body|html|head)>', '', Soup(markup).prettify()).strip()
