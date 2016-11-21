# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import cgi
import codecs
import re

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML


class Null:
    def render(self, props):
        return DOM.create_element()


class Image:
    def render(self, props):
        data = props.get('data', {})

        return DOM.create_element('img', {
            'src': data.get('src'),
            'width': data.get('width'),
            'height': data.get('height'),
            'alt': data.get('alt'),
        })


class Link:
    def render(self, props):
        data = props.get('data', {})
        href = data['url']

        return DOM.create_element('a', {'href': href}, props['children'])


class URLDecorator:
    """
    Replace plain urls with actual hyperlinks.
    """
    SEARCH_RE = re.compile(r'(http://|https://|www\.)([a-zA-Z0-9\.\-%/\?&_=\+#:~!,\'\*\^$]+)')

    def __init__(self, new_window=False):
        self.new_window = new_window

    def replace(self, match):
        u_protocol = match.group(1)
        u_href = match.group(2)
        u_href = u_protocol + u_href

        text = cgi.escape(u_href)
        if u_href.startswith("www"):
            u_href = "http://" + u_href
        props = {'href': u_href}
        if self.new_window:
            props.update(target="_blank")

        return DOM.create_element('a', props, text)


class HashTagDecorator:
    """
    Wrap hash tags in spans with specific class.
    """

    SEARCH_RE = re.compile(r'#\w+')

    def replace(self, match):
        return DOM.create_element('em', {'class': 'hash_tag'}, match.group(0))


config = {
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(),
        ENTITY_TYPES.IMAGE: Image(),
        ENTITY_TYPES.TOKEN: Null(),
    },
    'composite_decorators': [
        URLDecorator(),
        HashTagDecorator(),
    ],
    # Extend/override the default block map.
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.HEADER_TWO: {
            'element': ['h2', {'className': 'c-amazing-heading'}],
            'wrapper': 'div',
        },
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': ['ul', {'className': 'bullet-list'}],
        },
    }),
    # Extend/override the default style map.
    'style_map': dict(STYLE_MAP, **{
        'HIGHLIGHT': {'element': 'strong', 'textDecoration': 'underline'},
    }),
}

exporter = HTML(config)

content_state = {
    'entityMap': {
        '0': {
            'type': 'LINK',
            'mutability': 'MUTABLE',
            'data': {
                'url': 'http://example.com',
            },
        },
        '1': {
            'type': 'LINK',
            'mutability': 'MUTABLE',
            'data': {
                'url': 'https://www.springload.co.nz/work/nz-festival/',
            },
        },
        '2': {
            'type': 'TOKEN',
            'mutability': 'IMMUTABLE',
            'data': {},
        },
    },
    'blocks': [
        {
            'key': '6mgfh',
            'text': 'User experience (UX) design',
            'type': 'header-two',
            'depth': 0,
            'inlineStyleRanges': [
                {
                    'offset': 16,
                    'length': 4,
                    'style': 'BOLD'
                },
                {
                    'offset': 16,
                    'length': 4,
                    'style': 'CODE'
                },
            ],
            'entityRanges': []
        },
        {
            'key': '5384u',
            'text': 'Everyone 🍺 Springload applies the best #principles of UX to their work. (https://www.springload.co.nz/work/nz-festival/)',
            'type': 'blockquote',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': 'eelkd',
            'text': 'The design decisions we make building #tools and #services for your customers are based on empathy for what your customers need.',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': 'b9grk',
            'text': 'User research',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': 'a1tis',
            'text': 'User testing and analysis',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [
                {
                    'offset': 0,
                    'length': 25,
                    'key': 0
                }
            ]
        },
        {
            'key': 'adjdn',
            'text': 'A/B testing',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': '62lio',
            'text': 'Prototyping',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': '62lio',
            'text': 'Beautiful <code/>',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': '672oo',
            'text': ' ',
            'type': 'horizontal-rule',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [
                {
                    'offset': 0,
                    'length': 1,
                    'key': 2,
                },
            ],
        },
        {
            'key': 'fq3f',
            'text': 'How we made it delightful and easy for people to find NZ Festival shows',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [
                {
                    'offset': 0,
                    'length': 71,
                    'key': 1
                }
            ]
        },
        {
            'key': '93agv',
            'text': '1. A list item (0)',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '4ht9m',
            'text': '2. Oops! (1)',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c6gc4',
            'text': '3. Does this support nesting? (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c6gc3',
            'text': '4. Maybe? (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '3mn5b',
            'text': '5. Yep it does! (3)',
            'type': 'unordered-list-item',
            'depth': 3,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '28umf',
            'text': '6. How many levels deep? (4)',
            'type': 'unordered-list-item',
            'depth': 4,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c2gc4',
            'text': '7. Backtracking, two at once... (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1gcb',
            'text': '8. Uh oh (1)',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c2gh4',
            'text': '9. Up, up, and away! (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1ghb',
            'text': '10. Arh! (1)',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1gc9',
            'text': '11. Did this work? (0)',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1gc9',
            'text': '12. Yes! (0)',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
    ]
}

markup = exporter.render(content_state)
pretty = DOM.pretty_print(markup)

# Display in console.
print(pretty)

# Output to a file
with codecs.open('example.html', 'w', 'utf-8') as file:
    file.write('<!DOCTYPE html><html><head><meta charset="utf-8" /><title>Test</title></head><body>\n{pretty}\n</body></html>'.format(pretty=pretty))
