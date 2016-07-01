from __future__ import absolute_import, unicode_literals

import json
import os
import unittest

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.entities.image import Image
from draftjs_exporter.entities.link import Link
from draftjs_exporter.html import HTML

fixtures_path = os.path.join(os.path.dirname(__file__), 'test_exports.json')
fixtures = json.loads(open(fixtures_path, 'r').read())

config = {
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(),
        ENTITY_TYPES.IMAGE: Image(),
    },
    'block_map': {
        BLOCK_TYPES.HEADER_ONE: {'element': 'h1'},
        BLOCK_TYPES.HEADER_TWO: {'element': 'h2'},
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': ['ul', {}],
        },
        BLOCK_TYPES.ORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': ['ol', {}],
        },
        BLOCK_TYPES.UNSTYLED: {'element': 'p'},
        BLOCK_TYPES.ATOMIC: {'element': 'span'},
    },
    'style_map': {
        INLINE_STYLES.ITALIC: {'element': 'em'},
        INLINE_STYLES.BOLD: {'element': 'strong'},
    },
}


class TestExports(unittest.TestCase):
    # TODO Find a way to have one test case per case in the JSON file
    def test_exports(self):
        for export in fixtures:
            exporter = HTML(config)
            self.assertEqual(exporter.call(export.get('content_state')), export.get('output'))
