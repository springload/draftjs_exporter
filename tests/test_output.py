# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import BLOCK_MAP
from draftjs_exporter.entities import Link, Null
from draftjs_exporter.entity_state import EntityException
from draftjs_exporter.html import HTML

config = {
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(),
        ENTITY_TYPES.TOKEN: Null(),
    },
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': ['ul', {'className': 'steps'}],
        },
        BLOCK_TYPES.ATOMIC: {'element': 'span'},
    }),
    'style_map': {
        INLINE_STYLES.ITALIC: {'element': 'em'},
        INLINE_STYLES.BOLD: {'element': 'strong'},
        'HIGHLIGHT': {'element': 'strong', 'textDecoration': 'underline'},
    },
}


class TestOutput(unittest.TestCase):
    """
    Test cases related to specific features of the HTML builder.
    """
    def setUp(self):
        self.maxDiff = None
        self.exporter = HTML(config)

    def test_render_empty(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': []
        }), '')

    def test_render_emptiest(self):
        self.assertEqual(self.exporter.render({}), '')

    def test_render_with_different_blocks(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'Header',
                    'type': 'header-one',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                }
            ]
        }), '<h1>Header</h1><p>some paragraph text</p>')

    def test_render_with_unicode(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'Emojis! 🍺',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                }
            ]
        }), '<p>Emojis! \U0001f37a</p>')

    def test_render_with_inline_styles(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'ITALIC'
                        }
                    ],
                    'entityRanges': []
                }
            ]
        }), '<p><em>some</em> paragraph text</p>')

    def test_render_with_multiple_inline_styles(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {
                '0': {
                    'type': 'LINK',
                    'mutability': 'MUTABLE',
                    'data': {
                        'url': 'http://example.com'
                    }
                }
            },
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'Header',
                    'type': 'header-one',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 2,
                            'style': 'BOLD'
                        }
                    ],
                    'entityRanges': []
                },
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'HIGHLIGHT'
                        }
                    ],
                    'entityRanges': [
                        {
                            'offset': 5,
                            'length': 9,
                            'key': 0
                        }
                    ]
                }
            ]
        }), '<h1><strong>He</strong>ader</h1><p><strong style="text-decoration: underline;">some</strong> <a href="http://example.com">paragraph</a> text</p>')

    def test_render_with_entities(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {
                '0': {
                    'type': 'LINK',
                    'mutability': 'MUTABLE',
                    'data': {
                        'url': 'http://example.com'
                    }
                }
            },
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': [
                        {
                            'offset': 5,
                            'length': 9,
                            'key': 0
                        }
                    ]
                }
            ]
        }), '<p>some <a href="http://example.com">paragraph</a> text</p>')

    def test_render_with_entities_crossing_raises(self):
        with self.assertRaises(EntityException):
            self.exporter.render({
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
                            'url': 'http://bar.example.com'
                        }
                    }
                },
                'blocks': [
                    {
                        'key': 'dem5p',
                        'text': 'some paragraph text',
                        'type': 'unstyled',
                        'depth': 0,
                        'inlineStyleRanges': [],
                        'entityRanges': [
                            {
                                'offset': 5,
                                'length': 9,
                                'key': 0
                            },
                            {
                                'offset': 2,
                                'length': 9,
                                'key': 1
                            }
                        ]
                    }
                ]
            })

    def test_render_with_wrapping(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': [],
                },
                {
                    'key': 'dem5p',
                    'text': 'item2',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                }
            ]
        }), '<ul class="steps"><li>item1</li><li>item2</li></ul>')

    def test_render_with_number_attribute(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                    'element': 'li',
                    'wrapper': ['ul', {'length': 5}],
                },
            }),
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ],
        }), '<ul length="5"><li>item1</li></ul>')

    def test_render_with_boolean_attribute_true(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                    'element': 'li',
                    'wrapper': ['ul', {'disabled': True}],
                },
            }),
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ],
        }), '<ul disabled="True"><li>item1</li></ul>')

    def test_render_with_boolean_attribute_false(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                    'element': 'li',
                    'wrapper': ['ul', {'disabled': False}],
                },
            }),
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ]
        }), '<ul disabled="False"><li>item1</li></ul>')

    def test_render_with_none_attribute(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                    'element': 'li',
                    'wrapper': ['ul', {'disabled': None}],
                },
            }),
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ],
        }), '<ul><li>item1</li></ul>')

    def test_render_with_unknown_attribute(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                    'element': 'li',
                    'wrapper': ['ul', {'*ngFor': 'test'}],
                },
            })
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ],
        }), '<ul *ngfor="test"><li>item1</li></ul>')

    def test_render_with_element_options(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.HEADER_TWO: {
                    'element': ['h2', {'className': 'c-amazing-heading'}],
                },
            })
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'header-two',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ],
        }), '<h2 class="c-amazing-heading">item1</h2>')

    def test_render_with_token_entity(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {
                '2': {
                    'type': 'TOKEN',
                    'mutability': 'IMMUTABLE',
                    'data': {},
                },
            },
            'blocks': [
                {
                    'key': 'dem1p',
                    'text': 'item1',
                    'type': 'unordered-list-item',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
                {
                    'key': 'dem5p',
                    'text': 'item2',
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
            ]
        }), '<ul class="steps"><li>item1</li><li>item2</li></ul><hr/>')

    def test_render_with_unidirectional_nested_wrapping(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
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
            ],
        }), '<ul class="steps"><li>A list item<ul class="steps"><li>Oops!<ul class="steps"><li>Does this support nesting?</li><li>Maybe?<ul class="steps"><li>Yep it does!<ul class="steps"><li>How many levels deep?</li><li>Lots.</li><li>Ah.</li></ul></li></ul></li></ul></li></ul></li></ul>')

    def test_render_with_backtracking_nested_wrapping(self):
        self.assertEqual(self.exporter.render({
            'entityMap': {},
            'blocks': [
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
            ],
        }), '<ul class="steps"><li>A list item (0)<ul class="steps"><li>Oops! (1)<ul class="steps"><li>Does this support nesting? (2)</li><li>Maybe? (2)<ul class="steps"><li>Yep it does! (3)<ul class="steps"><li>How many levels deep? (4)</li></ul></li></ul></li><li>Backtracking, two at once... (2)</li></ul></li><li>Uh oh (1)<ul class="steps"><li>Up, up, and away! (2)</li></ul></li><li>Arh! (1)</li></ul></li><li>Did this work? (0)</li><li>Yes! (0)</li></ul>')

    def test_render_with_big_content(self):
        self.assertEqual(HTML({
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
                'ITALIC': {'element': 'em'},
                'BOLD': {'element': 'strong'}
            }
        }).render({
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
        }), '<h2>User experience <strong>(UX)</strong> design</h2><blockquote>Everyone at Springload applies the best principles of UX to their work.</blockquote><p>The design decisions we make building tools and services for your customers are based on empathy for what your customers need.</p><ul><li>User research</li><li><a href="http://example.com">User testing and analysis</a></li><li>A/B testing</li><li>Prototyping</li></ul><p><a href="https://www.springload.co.nz/work/nz-festival/">How we made it delightful and easy for people to find NZ Festival shows</a></p>')

    def test_render_with_default_block_map(self):
        self.assertEqual(HTML({
            'style_map': {
                INLINE_STYLES.ITALIC: {'element': 'em'},
                INLINE_STYLES.BOLD: {'element': 'strong'},
                'HIGHLIGHT': {'element': 'strong', 'textDecoration': 'underline'},
            },
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'ITALIC'
                        }
                    ],
                    'entityRanges': []
                }
            ]
        }), '<p><em>some</em> paragraph text</p>')

    def test_render_with_default_style_map(self):
        self.assertEqual(HTML({
            'block_map': dict(BLOCK_MAP, **{
                BLOCK_TYPES.UNORDERED_LIST_ITEM: {
                    'element': 'li',
                    'wrapper': ['ul', {'className': 'steps'}],
                },
                BLOCK_TYPES.ATOMIC: {'element': 'span'},
            })
        }).render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'ITALIC'
                        }
                    ],
                    'entityRanges': []
                }
            ]
        }), '<p><em>some</em> paragraph text</p>')

    def test_render_with_default_config(self):
        self.assertEqual(HTML().render({
            'entityMap': {},
            'blocks': [
                {
                    'key': 'dem5p',
                    'text': 'some paragraph text',
                    'type': 'unstyled',
                    'depth': 0,
                    'inlineStyleRanges': [
                        {
                            'offset': 0,
                            'length': 4,
                            'style': 'ITALIC'
                        }
                    ],
                    'entityRanges': []
                }
            ]
        }), '<p><em>some</em> paragraph text</p>')
