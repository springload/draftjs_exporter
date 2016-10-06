from __future__ import absolute_import, unicode_literals

import re

from lxml import etree, html

# See http://stackoverflow.com/questions/7703018/how-to-write-namespaced-element-attributes-with-lxml
XLINK = 'http://www.w3.org/1999/xlink'


class DOM(object):
    """
    Wrapper around our HTML building library to facilitate changes.
    """
    @staticmethod
    def create_tag(type, attributes={}):
        return etree.Element(type, attrib=attributes)

    @staticmethod
    def create_element(type=None, props={}, *children):
        """
        Signature inspired by React.createElement.
        createElement(
          string/ReactClass type,
          [object props],
          [children ...]
        )
        https://facebook.github.io/react/docs/top-level-api.html#react.createelement
        """
        if not type:
            elt = DOM.create_document_fragment()
        else:
            attributes = {}

            # Map props from React/Draft.js to lxml lingo.
            if 'className' in props:
                props['class'] = props.get('className')
                props.pop('className', None)

            # TODO One-off fix ATM, even though the problem is everywhere.
            if 'xlink:href' in props:
                props['{%s}href' % XLINK] = props.get('xlink:href')
                props.pop('xlink:href', None)

            for key in props:
                prop = props[key]
                # Filter null values and cast to string for lxml
                if prop is not None:
                    attributes[key] = str(prop)

            elt = DOM.create_tag(type, attributes)

        for child in children:
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
        return html.fromstring(markup)

    @staticmethod
    def append_child(elt, child):
        elt.append(child)

    @staticmethod
    def set_attribute(elt, attr, value):
        elt.set(attr, value)

    @staticmethod
    def get_tag_name(elt):
        return elt.tag

    @staticmethod
    def get_class_list(elt):
        return [elt.get('class')]

    @staticmethod
    def get_text_content(elt):
        return elt.text

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
        return re.sub(r'</?(fragment|textnode)>', '', etree.tostring(elt, method='html').decode('utf-8'))

    @staticmethod
    def pretty_print(markup):
        """
        Convenience method.
        Pretty print the element, removing the top-level node that lxml needs.
        """
        return re.sub(r'</?doc>', '', etree.tostring(html.fromstring('<doc>%s</doc>' % markup), encoding='unicode', pretty_print=True))
