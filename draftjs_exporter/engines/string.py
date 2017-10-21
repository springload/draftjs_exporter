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

    @staticmethod
    def create_tag(type_, attr=None):
        return {
            'type': type_,
            'attr': attr,
            'children': [],
        }

    @staticmethod
    def parse_html(markup):
        return {
            'type': 'fragment',
            'attr': None,
            'children': [markup]
        }

    @staticmethod
    def append_child(elt, child):
        # This check is necessary because the current wrapper_state implementation
        # has an issue where it inserts elements multiple times.
        # This must be skipped for text, which can be duplicated.
        is_existing_ref = isinstance(child, dict) and child in elt['children']
        if not is_existing_ref:
            elt['children'].append(child)

    @staticmethod
    def render(elt):
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

        # TODO This list of self-closing tags is very naive / incomplete.
        if elt['type'] in ['br', 'img', 'hr']:
            rendered = '<{0}{1}/>'.format(elt['type'], attrs)
        elif elt['type'] == 'fragment':
            rendered = children
        else:
            rendered = '<{0}{1}>{2}</{0}>'.format(elt['type'], attrs, children)

        return rendered

    @staticmethod
    def render_debug(elt):
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

        # TODO This list of self-closing tags is very naive / incomplete.
        if elt['type'] in ['br', 'img', 'hr']:
            rendered = '<{0}{1}/>'.format(elt['type'], attrs)
        else:
            rendered = '<{0}{1}>{2}</{0}>'.format(elt['type'], attrs, children)

        return rendered
