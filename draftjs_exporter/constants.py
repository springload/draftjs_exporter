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
