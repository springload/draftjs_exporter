from __future__ import absolute_import, unicode_literals

import cProfile
import json
import os
import unittest
from pstats import Stats

import six

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import BLOCK_MAP
from draftjs_exporter.html import HTML
from tests.test_composite_decorators import Hashtag, Linkify
from tests.test_entities import Image, Link

fixtures_path = os.path.join(os.path.dirname(__file__), 'test_exports.json')
fixtures = json.loads(open(fixtures_path, 'r').read())

exporter = HTML({
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link,
        ENTITY_TYPES.IMAGE: Image,
    },
    'composite_decorators': [
        Linkify,
        Hashtag,
    ],
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': ['ul', {'className': 'bullet-list'}],
        },
    }),
    'style_map': {
        INLINE_STYLES.ITALIC: {'element': 'em'},
        INLINE_STYLES.BOLD: {'element': 'strong'},
    },
})


class TestExportsMeta(type):
    """
    Generates test cases dynamically.
    See http://stackoverflow.com/a/20870875/1798491
    """
    def __new__(mcs, name, bases, dict):
        def gen_test(export):
            def test(self):
                self.maxDiff = None
                self.assertEqual(exporter.render(export.get('content_state')), export.get('output'))
            return test

        for export in fixtures:
            test_name = 'test_export_%s' % export.get('label').lower().replace(' ', '_')
            dict[test_name] = gen_test(export)

        return type.__new__(mcs, name, bases, dict)


class TestExports(six.with_metaclass(TestExportsMeta, unittest.TestCase)):
    @classmethod
    def setUpClass(cls):
        cls.pr = cProfile.Profile()
        cls.pr.enable()

    @classmethod
    def tearDownClass(cls):
        cls.pr.disable()
        p = Stats(cls.pr)
        p.strip_dirs().sort_stats('cumulative').print_stats(20)

    def test_init(self):
        self.assertIsInstance(exporter, HTML)


if __name__ == "__main__":
    unittest.main()
