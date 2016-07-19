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
    def create_element(type=None, props=None, *children):
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
            # Map props from React/Draft.js to lxml lingo.
            if props:
                if 'className' in props:
                    props['class'] = props.get('className')
                    props.pop('className', None)

                # TODO Should be in a separate, reusable factory
                if 'xlink:href' in props:
                    props['{%s}href' % XLINK] = props.get('xlink:href')
                    props.pop('xlink:href', None)

            elt = etree.Element(type, attrib=props)

        for child in children:
            if hasattr(child, 'tag'):
                DOM.append_child(elt, child)
            else:
                elt.text = elt.text + child if elt.text else child

        return elt

    @staticmethod
    def create_document_fragment():
        return etree.Element('fragment')

    @staticmethod
    def create_text_node(text):
        elt = etree.Element('textnode')
        DOM.set_text_content(elt, text)
        return elt

    @staticmethod
    def append_child(elt, child):
        elt.append(child)

    @staticmethod
    def set_attribute(elt, attr, value):
        elt.set(attr, value)

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
