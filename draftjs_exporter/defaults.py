from __future__ import absolute_import, unicode_literals

from draftjs_exporter.constants import BLOCK_TYPES, INLINE_STYLES

# Default block map to extend.
BLOCK_MAP = {
    BLOCK_TYPES.UNSTYLED: 'p',
    BLOCK_TYPES.HEADER_ONE: 'h1',
    BLOCK_TYPES.HEADER_TWO: 'h2',
    BLOCK_TYPES.HEADER_THREE: 'h3',
    BLOCK_TYPES.HEADER_FOUR: 'h4',
    BLOCK_TYPES.HEADER_FIVE: 'h5',
    BLOCK_TYPES.HEADER_SIX: 'h6',
    BLOCK_TYPES.UNORDERED_LIST_ITEM: {'element': 'li', 'wrapper': 'ul'},
    BLOCK_TYPES.ORDERED_LIST_ITEM: {'element': 'li', 'wrapper': 'ol'},
    BLOCK_TYPES.BLOCKQUOTE: 'blockquote',
    # TODO Ideally would want double wrapping in pre + code.
    # See https://github.com/sstur/draft-js-export-html/blob/master/src/stateToHTML.js#L88
    BLOCK_TYPES.CODE: 'pre',
    BLOCK_TYPES.ATOMIC: lambda props: props['children'],
}

# Default style map to extend.
# Tags come from https://developer.mozilla.org/en-US/docs/Web/HTML/Element.
# and are loosely aligned with https://github.com/jpuri/draftjs-to-html.
# Only styles that map to HTML elements are allowed as defaults.
STYLE_MAP = {
    INLINE_STYLES.BOLD: 'strong',
    INLINE_STYLES.CODE: 'code',
    INLINE_STYLES.ITALIC: 'em',
    INLINE_STYLES.UNDERLINE: 'u',
    INLINE_STYLES.STRIKETHROUGH: 's',
    INLINE_STYLES.SUPERSCRIPT: 'sup',
    INLINE_STYLES.SUBSCRIPT: 'sub',
    INLINE_STYLES.MARK: 'mark',
    INLINE_STYLES.QUOTATION: 'q',
    INLINE_STYLES.SMALL: 'small',
    INLINE_STYLES.SAMPLE: 'samp',
    INLINE_STYLES.INSERT: 'ins',
    INLINE_STYLES.DELETE: 'del',
    INLINE_STYLES.KEYBOARD: 'kbd',
}
