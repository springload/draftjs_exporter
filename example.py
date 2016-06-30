from __future__ import absolute_import, unicode_literals

from draftjs_exporter.entities.link import Link
from draftjs_exporter.html import HTML

config = {
    'entity_decorators': {
        'LINK': Link()
    },
    'block_map': {
        'header-two': {'element': 'h2'},
        'blockquote': {'element': 'blockquote'},
        'unordered-list-item': {
            'element': 'li',
            'wrapper': ['ul', {}]
        },
        'unstyled': {'element': 'p'}
    },
    'style_map': {
        'ITALIC': {'fontStyle': 'italic'},
        'BOLD': {'fontStyle': 'bold'}
    }
}

exporter = HTML(config)

content_state = {
    'entityMap': {
        '0': {
            'type': 'LINK',
            'mutability': 'MUTABLE',
            'data': {
                'url': 'http://example.com'
            }
        },
        '1': {
            'type': 'LINK',
            'mutability': 'MUTABLE',
            'data': {
                'url': 'https://www.springload.co.nz/work/nz-festival/'
            }
        }
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
            'text': ' The design decisions we make building tools and services for your customers are based on empathy for what your customers need.',
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
        }
    ]
}


markup = exporter.call(content_state)
print (markup)
