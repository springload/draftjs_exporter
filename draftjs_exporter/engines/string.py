from __future__ import absolute_import, unicode_literals

import html

from draftjs_exporter.engines.base import DOMEngine

# TODO This list of self-closing tags is very naive / incomplete.
SELF_CLOSING_TAGS = ['br', 'img', 'hr']


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
    def append_child(elt, child):
        # This check is necessary because the current wrapper_state implementation
        # has an issue where it inserts elements multiple times.
        # This must be skipped for text, which can be duplicated.
        is_existing_ref = isinstance(child, dict) and child in elt['children']
        if not is_existing_ref:
            elt['children'].append(child)

    @staticmethod
    def render_attrs(attr):
        attrs = [' {0}="{1}"'.format(a, html.escape(attr[a])) for a in attr]
        return ''.join(sorted(attrs))

    @staticmethod
    def render_children(children):
        rendered = ''
        for c in children:
            if isinstance(c, dict):
                rendered += DOM_STRING.render(c)
            else:
                rendered += html.escape(c)

        return rendered

    @staticmethod
    def render(elt):
        attr = ''
        if elt['attr']:
            attr = DOM_STRING.render_attrs(elt['attr'])

        children = ''
        if len(elt['children']) != 0:
            children = DOM_STRING.render_children(elt['children'])

        if elt['type'] in SELF_CLOSING_TAGS:
            rendered = '<{0}{1}/>'.format(elt['type'], attr)
        elif elt['type'] == 'fragment':
            rendered = children
        else:
            rendered = '<{0}{1}>{2}</{0}>'.format(elt['type'], attr, children)

        return rendered

    @staticmethod
    def render_debug(elt):
        attr = ''
        if elt['attr']:
            attr = DOM_STRING.render_attrs(elt['attr'])

        children = ''
        if len(elt['children']) != 0:
            children = DOM_STRING.render_children(elt['children'])

        if elt['type'] in SELF_CLOSING_TAGS:
            rendered = '<{0}{1}/>'.format(elt['type'], attr)
        else:
            rendered = '<{0}{1}>{2}</{0}>'.format(elt['type'], attr, children)

        return rendered
