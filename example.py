# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import codecs
import cProfile
import re
from pstats import Stats

# draftjs_exporter provides default configurations and predefined constants for reuse.
from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML


def Blockquote(props):
    block_data = props['block']['data']

    return DOM.create_element('blockquote', {
        'cite': block_data.get('cite')
    })


def ListItem(props):
    depth = props['block']['depth']

    return DOM.create_element('li', {
        'class': 'list-item--depth-{0}'.format(depth)
    })


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
    # `block_map` is a mapping from Draft.js block types to a definition of their HTML representation.
    # Extend BLOCK_MAP to start with sane defaults, or make your own from scratch.
    'block_map': dict(BLOCK_MAP, **{
        # The most basic mapping format, block type to tag name.
        BLOCK_TYPES.HEADER_TWO: 'h2',
        # Use a dict to define props on the block.
        BLOCK_TYPES.HEADER_THREE: {'element': 'h3', 'props': {'className': 'u-text-center'}},
        # Add a wrapper (and wrapper_props) to wrap adjacent blocks.
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': 'ul',
            'wrapper_props': {'className': 'bullet-list'},
        },
        # Use a component for more flexibility (reading block data or depth).
        BLOCK_TYPES.BLOCKQUOTE: Blockquote,
        BLOCK_TYPES.ORDERED_LIST_ITEM: {
            'element': ListItem,
            'wrapper': 'ol',
        }
    }),
    # `style_map` defines the HTML representation of inline elements.
    # Extend STYLE_MAP to start with sane defaults, or make your own from scratch.
    'style_map': dict(STYLE_MAP, **{
        # Use the same mapping format as in the `block_map`.
        'KBD': 'kbd',
        'STRIKETHROUGH': {'element': 'span', 'props': {'className': 'u-strikethrough'}},
        'HIGHLIGHT': {'element': 'strong', 'props': {'style': {'textDecoration': 'underline'}}},
    }),
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(use_new_window=True),
        ENTITY_TYPES.IMAGE: Image,
        ENTITY_TYPES.HORIZONTAL_RULE: HR,
    },
    'composite_decorators': [
        BR,
        Hashtag,
    ],
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
            'key': '6bvvh',
            'text': 'Front-end (FED) development',
            'type': 'header-three',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': '5384u',
            'text': 'Everyone 🍺 Springload applies the best #principles of UX to their work.',
            'type': 'blockquote',
            'depth': 0,
            'data': {
                'cite': 'http://example.com/',
            },
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
            'type': 'ordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': 'a1tis',
            'text': 'User testing and analysis',
            'type': 'ordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [
                {
                    'offset': 13,
                    'length': 12,
                    'style': 'STRIKETHROUGH'
                },
            ],
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
            'type': 'ordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': '62lio',
            'text': 'Prototyping',
            'type': 'ordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': '62lio',
            'text': 'Beautiful <code/>',
            'type': 'ordered-list-item',
            'depth': 1,
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
        {
            'key': '33gc9',
            'text': 'Use cmd + b to style text as bold',
            'type': 'unstyled',
            'depth': 0,
            'inlineStyleRanges': [
                {
                    'offset': 4,
                    'length': 7,
                    'style': 'KBD'
                },
            ],
            'entityRanges': [],
        },
    ]
}

pr = cProfile.Profile()
pr.enable()

markup = exporter.render(content_state)

pr.disable()
p = Stats(pr)

pretty = DOM.pretty_print(markup)

# Display in console.
print(pretty)

p.strip_dirs().sort_stats('cumulative').print_stats(0)

# Output to a file
with codecs.open('example.html', 'w', 'utf-8') as file:
    file.write('<!DOCTYPE html><html><head><meta charset="utf-8" /><title>Test</title></head><body>\n{pretty}\n</body></html>'.format(pretty=pretty))
