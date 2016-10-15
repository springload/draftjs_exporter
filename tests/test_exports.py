from __future__ import absolute_import, unicode_literals

import json
import os
import unittest

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import BLOCK_MAP
from draftjs_exporter.entities import Image, Link
from draftjs_exporter.html import HTML

fixtures_path = os.path.join(os.path.dirname(__file__), 'test_exports.json')
fixtures = json.loads(open(fixtures_path, 'r').read())

# TODO Move this to JSON file.
config = {
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link(),
        ENTITY_TYPES.IMAGE: Image(),
    },
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': ['ul', {'className': 'bullet-list'}],
        },
        BLOCK_TYPES.ATOMIC: {'element': 'span'},
    }),
    'style_map': {
        INLINE_STYLES.ITALIC: {'element': 'em'},
        INLINE_STYLES.BOLD: {'element': 'strong'},
    },
}


class TestExportsMeta(type):
    """
    Generates test cases dynamically.
    See http://stackoverflow.com/a/20870875/1798491
    """
    def __new__(mcs, name, bases, dict):
        def gen_test(export):
            def test(self):
                self.maxDiff = None
                self.assertEqual(HTML(config).render(export.get('content_state')), export.get('output'))
            return test

        for export in fixtures:
            test_name = 'test_export_%s' % export.get('label').lower().replace(' ', '_')
            dict[test_name] = gen_test(export)

        return type.__new__(mcs, name, bases, dict)


class TestExports(unittest.TestCase):
    __metaclass__ = TestExportsMeta
