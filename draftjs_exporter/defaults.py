from __future__ import absolute_import, unicode_literals

from draftjs_exporter.constants import BLOCK_TYPES, INLINE_STYLES

# Default block map to extend.
BLOCK_MAP = {
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
STYLE_MAP = {
    INLINE_STYLES.ITALIC: {'element': 'em'},
    INLINE_STYLES.BOLD: {'element': 'strong'},
    INLINE_STYLES.CODE: {'element': 'code'},
    INLINE_STYLES.STRIKETHROUGH: {'textDecoration': 'line-through'},
    INLINE_STYLES.UNDERLINE: {'textDecoration': 'underline'},
}
