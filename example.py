# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import codecs
import re

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML


def HR(props):
    return DOM.create_element('hr')


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
    def __init__(self, use_new_window=False):
        self.use_new_window = use_new_window

    def render(self, props):
        data = props.get('data', {})
        link_props = {
            'href': data['url'],
        }

        if self.use_new_window:
            link_props['target'] = '_blank'
            link_props['rel'] = 'noreferrer noopener'

        return DOM.create_element('a', link_props, props['children'])


class BR:
    """
    Replace line breaks (\n) with br tags.
    """
    SEARCH_RE = re.compile(r'\n')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block_type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('br')


class Hashtag:
    """
    Wrap hashtags in spans with a specific class.
    """
    SEARCH_RE = re.compile(r'#\w+')

    def render(self, props):
        # Do not process matches inside code blocks.
        if props['block_type'] == BLOCK_TYPES.CODE:
            return props['children']

        return DOM.create_element('span', {'class': 'hashtag'}, props['children'])


config = {
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(use_new_window=True),
        ENTITY_TYPES.IMAGE: Image,
        ENTITY_TYPES.HORIZONTAL_RULE: HR,
    },
    'composite_decorators': [
        BR,
        Hashtag,
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
            'type': 'HORIZONTAL_RULE',
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
            'text': 'Everyone 🍺 Springload applies the best #principles of UX to their work.',
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
            'type': 'atomic',
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
            'text': 'How we made it delightful\nand easy for people to find NZ Festival shows',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [
                {
                    'offset': 53,
                    'length': 12,
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
