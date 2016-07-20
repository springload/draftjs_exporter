from __future__ import absolute_import, unicode_literals


# http://stackoverflow.com/a/22723724/1798491
class Enum(object):
    def __init__(self, tupleList):
        self.tupleList = tupleList

    def __getattr__(self, name):
        return name


# https://github.com/draft-js-utils/draft-js-utils/blob/master/src/Constants.js
class BLOCK_TYPES:
    UNSTYLED = 'unstyled'
    HEADER_ONE = 'header-one'
    HEADER_TWO = 'header-two'
    HEADER_THREE = 'header-three'
    HEADER_FOUR = 'header-four'
    HEADER_FIVE = 'header-five'
    HEADER_SIX = 'header-six'
    UNORDERED_LIST_ITEM = 'unordered-list-item'
    ORDERED_LIST_ITEM = 'ordered-list-item'
    BLOCKQUOTE = 'blockquote'
    PULLQUOTE = 'pullquote'
    CODE = 'code-block'
    ATOMIC = 'atomic'
    HORIZONTAL_RULE = 'horizontal-rule'

ENTITY_TYPES = Enum(('LINK', 'IMAGE', 'TOKEN'))

INLINE_STYLES = Enum(('BOLD', 'CODE', 'ITALIC', 'STRIKETHROUGH', 'UNDERLINE'))

# Default block map to extend.
DEFAULT_BLOCK_MAP = {
    BLOCK_TYPES.UNSTYLED: {'element': 'p'},
    BLOCK_TYPES.HEADER_ONE: {'element': 'h1'},
    BLOCK_TYPES.HEADER_TWO: {'element': 'h2'},
    BLOCK_TYPES.HEADER_THREE: {'element': 'h3'},
    BLOCK_TYPES.HEADER_FOUR: {'element': 'h4'},
    BLOCK_TYPES.HEADER_FIVE: {'element': 'h5'},
    BLOCK_TYPES.HEADER_SIX: {'element': 'h6'},
    BLOCK_TYPES.UNORDERED_LIST_ITEM: {'element': 'li', 'wrapper': ['ul', {}]},
    BLOCK_TYPES.ORDERED_LIST_ITEM: {'element': 'li', 'wrapper': ['ol', {}]},
    BLOCK_TYPES.BLOCKQUOTE: {'element': 'blockquote'},
    # TODO Ideally would want double wrapping in pre + code.
    # See https://github.com/sstur/draft-js-export-html/blob/master/src/stateToHTML.js#L88
    BLOCK_TYPES.CODE: {'element': 'pre'},
    BLOCK_TYPES.HORIZONTAL_RULE: {'element': 'hr'},
}

# Default style map to extend.
DEFAULT_STYLE_MAP = {
    INLINE_STYLES.ITALIC: {'element': 'em'},
    INLINE_STYLES.BOLD: {'element': 'strong'},
    INLINE_STYLES.CODE: {'element': 'code'},
    INLINE_STYLES.STRIKETHROUGH: {'textDecoration': 'line-through'},
    INLINE_STYLES.UNDERLINE: {'textDecoration': 'underline'},
}
