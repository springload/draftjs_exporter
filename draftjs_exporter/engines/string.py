from __future__ import absolute_import, unicode_literals

import html

from draftjs_exporter.engines.base import DOMEngine

# Python 2/3 unicode compatibility hack.
# See http://stackoverflow.com/questions/6812031/how-to-make-unicode-string-with-python3
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    def unicode(s):
        return str(s)


class DOM_STRING(DOMEngine):
    """
    string concat implementation of the DOM API.
    """

    key = 0
    rendered_keys = []

    @staticmethod
    def create_tag(type_, attr=None):
        DOM_STRING.key += 1
        return {
            'key': DOM_STRING.key,
            'type_': type_,
            'attr': attr,
            'children': [],
        }

    @staticmethod
    def append_child(elt, child):
        elt['children'].append(child)

    @staticmethod
    def render(elt):
        if elt['key'] in DOM_STRING.rendered_keys:
            return ''
        else:
            DOM_STRING.rendered_keys.append(elt['key'])

        attrs = ''
        if elt['attr']:
            for a in elt['attr']:
                attrs += ' {0}="{1}"'.format(a, html.escape(elt['attr'][a]))

        children = ''
        for c in elt['children']:
            if isinstance(c, dict):
                children += DOM_STRING.render(c)
            else:
                children += html.escape(c)

        if elt['type_'] in ['br', 'img', 'hr']:
            return '<{0}{1}/>'.format(elt['type_'], attrs)
        elif elt['type_'] == 'fragment':
            return children
        else:
            return '<{0}{1}>{2}</{0}>'.format(elt['type_'], attrs, children)

    @staticmethod
    def render_debug(elt):
        return elt
