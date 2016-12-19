from __future__ import absolute_import, unicode_literals


# http://stackoverflow.com/a/22723724/1798491
class Enum(object):
    def __init__(self, *elements):
        self.elements = tuple(elements)

    def __getattr__(self, name):
        if name not in self.elements:
            raise AttributeError("'Enum' has no attribute '{}'".format(name))

        return name


# https://github.com/facebook/draft-js/blob/master/src/model/constants/DraftBlockType.js
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
    CODE = 'code-block'
    ATOMIC = 'atomic'


ENTITY_TYPES = Enum('LINK', 'IMAGE', 'HORIZONTAL_RULE')

INLINE_STYLES = Enum('BOLD', 'CODE', 'ITALIC', 'STRIKETHROUGH', 'UNDERLINE')
