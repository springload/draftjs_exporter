from __future__ import absolute_import, unicode_literals

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.entities.image import Image
from draftjs_exporter.entities.link import Link
from draftjs_exporter.entities.token import Token
from draftjs_exporter.html import HTML

# TODO Support dt/dd, hr, br, cite, mark, q, s, sub, sup, video?
config = {
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(),
        ENTITY_TYPES.IMAGE: Image(),
        ENTITY_TYPES.TOKEN: Token(),
    },
    # Extend/override the default block map.
    'block_map': dict(BLOCK_MAP, **{
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
                }
            ],
            'entityRanges': []
        },
        {
            'key': '5384u',
            'text': 'Everyone at Springload applies the best principles of UX to their work.',
            'type': 'blockquote',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': []
        },
        {
            'key': 'eelkd',
            'text': 'The design decisions we make building tools and services for your customers are based on empathy for what your customers need.',
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
            'text': 'A list item (0)',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '4ht9m',
            'text': 'Oops! (1)',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c6gc4',
            'text': 'Does this support nesting? (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c6gc3',
            'text': 'Maybe? (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '3mn5b',
            'text': 'Yep it does! (3)',
            'type': 'unordered-list-item',
            'depth': 3,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '28umf',
            'text': 'How many levels deep? (4)',
            'type': 'unordered-list-item',
            'depth': 4,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c2gc4',
            'text': 'Backtracking, two at once... (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1gcb',
            'text': 'Uh oh (1)',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c2gh4',
            'text': 'Up, up, and away! (2)',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1ghb',
            'text': 'Arh! (1)',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1gc9',
            'text': 'Did this work? (0)',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c1gc9',
            'text': 'Yes! (0)',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
    ]
}

markup = exporter.call(content_state)
print(DOM.pretty_print(markup))
