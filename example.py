from __future__ import absolute_import, unicode_literals

from lxml import etree, html

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
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
    'block_map': {
        BLOCK_TYPES.UNSTYLED: {'element': 'p'},
        BLOCK_TYPES.HEADER_ONE: {'element': 'h1'},
        BLOCK_TYPES.HEADER_TWO: {'element': 'h2'},
        BLOCK_TYPES.HEADER_THREE: {'element': 'h3'},
        BLOCK_TYPES.HEADER_FOUR: {'element': 'h4'},
        BLOCK_TYPES.HEADER_FIVE: {'element': 'h5'},
        BLOCK_TYPES.HEADER_SIX: {'element': 'h6'},
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {'element': 'li', 'wrapper': ['ul', {'className': 'bullet-list'}]},
        BLOCK_TYPES.ORDERED_LIST_ITEM: {'element': 'li', 'wrapper': ['ol', {}]},
        BLOCK_TYPES.BLOCKQUOTE: {'element': 'blockquote'},
        # TODO Ideally would want double wrapping in pre + code.
        # See https://github.com/sstur/draft-js-export-html/blob/master/src/stateToHTML.js#L88
        BLOCK_TYPES.CODE: {'element': 'pre'},
        BLOCK_TYPES.HORIZONTAL_RULE: {'element': 'hr'},
    },
    'style_map': {
        INLINE_STYLES.ITALIC: {'element': 'em'},
        INLINE_STYLES.BOLD: {'element': 'strong'},
        INLINE_STYLES.CODE: {'element': 'code'},
        INLINE_STYLES.STRIKETHROUGH: {'textDecoration': 'line-through'},
        INLINE_STYLES.UNDERLINE: {'textDecoration': 'underline'},
    },
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
            'text': 'A list item',
            'type': 'unordered-list-item',
            'depth': 0,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '4ht9m',
            'text': 'Oops!',
            'type': 'unordered-list-item',
            'depth': 1,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c6gc4',
            'text': 'Does this support nesting?',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'c6gc3',
            'text': 'Maybe?',
            'type': 'unordered-list-item',
            'depth': 2,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '3mn5b',
            'text': 'Yep it does!',
            'type': 'unordered-list-item',
            'depth': 3,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': '28umf',
            'text': 'How many levels deep?',
            'type': 'unordered-list-item',
            'depth': 4,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'd81ns',
            'text': 'Lots.',
            'type': 'unordered-list-item',
            'depth': 4,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
        {
            'key': 'b0tsc',
            'text': 'Ah.',
            'type': 'unordered-list-item',
            'depth': 4,
            'inlineStyleRanges': [],
            'entityRanges': [],
        },
    ]
}

markup = exporter.call(content_state)
# Pretty print the markup, removing the top-level node that lxml adds.
document_root = html.fromstring('<root>%s</root>' % markup)
print(etree.tostring(document_root, encoding='unicode', pretty_print=True).replace('<root>', '').replace('</root>', ''))
