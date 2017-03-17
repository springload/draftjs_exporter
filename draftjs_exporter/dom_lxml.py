from __future__ import absolute_import, unicode_literals

import inspect
import re

from lxml import etree, html

# Python 2/3 unicode compatibility hack.
# See http://stackoverflow.com/questions/6812031/how-to-make-unicode-string-with-python3
XLINK = 'http://www.w3.org/1999/xlink'

try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    def unicode(s):
        return str(s)

# https://gist.github.com/yahyaKacem/8170675
_first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def clean_str(s):
    if not isinstance(s, basestring):
        s = unicode(s)

    elif not isinstance(s, unicode):
        s = s.decode('utf8')
        # See http://stackoverflow.com/questions/8733233/filtering-out-certain-bytes-in-python
    return re.sub(u'[^\u0020-\uD7FF\u0009\u000A\u000D\uE000-\uFFFD\u10000-\u10FFFF]+', '', s)


class DOM_LXML(object):
    """
    Wrapper around our HTML building library to facilitate changes.
    """
    @staticmethod
    def create_tag(type_, attributes=None):
        return etree.Element(type_, attrib=attributes)

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
            attributes = {}

            # Map props from React/Draft.js to HTML lingo.
            if 'className' in props:
                props['class'] = props.pop('className')

            if 'xlink:href' in props:
                props['{%s}href' % XLINK] = props.pop('xlink:href')

            for key in props:
                prop = props[key]

                if key == 'style' and isinstance(prop, dict):
                    rules = ['{0}: {1};'.format(DOM_LXML.camel_to_dash(style), prop[style]) for style in prop.keys()]
                    prop = ''.join(sorted(rules))

                # Filter None values.
                if prop is not None:
                    attributes[key] = prop

            if len(children) and isinstance(children[0], (list, tuple)):
                children = children[0]

            if inspect.isclass(type_):
                elt = type_().render(attributes)
            elif callable(getattr(type_, 'render', None)):
                elt = type_.render(attributes)
            elif callable(type_):
                elt = type_(attributes)
            else:
                try:
                    attributes = {k: unicode(v) for k, v in props.items() if v is not None}
                except:
                    attributes = {k: clean_str(v) for k, v in props.items() if v is not None}

                elt = DOM_LXML.create_tag(type_, attributes)

            for child in children:
                DOM_LXML.append_child(elt, child)

        return elt

    @staticmethod
    def create_document_fragment():
        return DOM_LXML.create_tag('fragment')

    @staticmethod
    def create_text_node(text):
        elt = DOM_LXML.create_tag('textnode')
        DOM_LXML.set_text_content(elt, text)
        return elt

    @staticmethod
    def parse_html(markup):
        return html.fromstring(markup)

    @staticmethod
    def camel_to_dash(camel_cased_str):
        sub2 = _first_cap_re.sub(r'\1-\2', camel_cased_str)
        dashed_case_str = _all_cap_re.sub(r'\1-\2', sub2).lower()
        return dashed_case_str.replace('--', '-')

    @staticmethod
    def append_child(elt, child):
        if child not in (None, ''):
            if hasattr(child, 'tag'):
                elt.append(child)
            else:
                elt_text = DOM_LXML.get_text_content(elt) or ''
                try:
                    elt_text += child
                except:
                    elt_text += clean_str(child)
                DOM_LXML.set_text_content(elt, elt_text)

    @staticmethod
    def set_attribute(elt, attr, value):
        elt.set(attr, value)

    @staticmethod
    def get_tag_name(elt):
        return elt.tag

    @staticmethod
    def get_class_list(elt):
        class_name = elt.get('class')
        return re.split('\ +', class_name) if class_name else []

    @staticmethod
    def get_text_content(elt):
        return ''.join(elt.itertext())

    @staticmethod
    def set_text_content(elt, text):
        try:
            elt.text = text
        except:
            elt.text = clean_str(text)

    @staticmethod
    def get_children(elt):
        return elt.getchildren()

    @staticmethod
    def render(elt):
        """
        Removes the fragments that should not have HTML tags. Caveat of lxml.
        Dirty, but quite easy to understand.
        """
        return re.sub(r'</?(fragment|textnode)>', '',
                      etree.tostring(elt, method='xml', encoding=unicode))

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
