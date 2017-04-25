from __future__ import absolute_import, unicode_literals

import cProfile
import json
import os
import unittest
from pstats import Stats

import six

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML
from tests.test_composite_decorators import BR, Hashtag, Linkify
from tests.test_entities import HR, Image, Link

fixtures_path = os.path.join(os.path.dirname(__file__), 'test_exports.json')
fixtures = json.loads(open(fixtures_path, 'r').read())

engines = [
    'bs',
    'lxml',
]

exporter = HTML({
    'entity_decorators': {
        ENTITY_TYPES.LINK: Link,
        ENTITY_TYPES.IMAGE: Image,
        ENTITY_TYPES.HORIZONTAL_RULE: HR,
        ENTITY_TYPES.EMBED: None,
    },
    'composite_decorators': [
        BR,
        Linkify,
        Hashtag,
    ],
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': 'ul',
            'wrapper_props': {'class': 'bullet-list'},
        },
    }),
    'style_map': dict(STYLE_MAP, **{
        'KBD': 'kbd',
        'HIGHLIGHT': {'element': 'strong', 'props': {'style': {'textDecoration': 'underline'}}},
    }),
})


class TestExportsMeta(type):
    """
    Generates test cases dynamically.
    See http://stackoverflow.com/a/20870875/1798491
    """
    def __new__(mcs, name, bases, tests):
        def gen_test(export, engine):
            def test(self):
                self.maxDiff = None
                DOM.use(engine)
                self.assertEqual(exporter.render(export['content_state']), export['output'][engine])

            return test

        if name == 'TestExportsHTML5LIB':
            engine = 'html5lib'
        elif name == 'TestExportsLXML':
            engine = 'lxml'

        for export in fixtures:
            test_label = export['label'].lower().replace(' ', '_')
            test_name = 'test_export_{0}_{1}'.format(engine, test_label)
            tests[test_name] = gen_test(export, engine)


        return type.__new__(mcs, name, bases, tests)


class TestExportsHTML5LIB(six.with_metaclass(TestExportsMeta, unittest.TestCase)):
    @classmethod
    def setUpClass(cls):
        cls.pr = cProfile.Profile()
        cls.pr.enable()
        print('\nhtml5lib')

    @classmethod
    def tearDownClass(cls):
        cls.pr.disable()
        Stats(cls.pr).strip_dirs().sort_stats('cumulative').print_stats(0)

    def test_init_html5lib(self):
        self.assertIsInstance(exporter, HTML)


class TestExportsLXML(six.with_metaclass(TestExportsMeta, unittest.TestCase)):
    @classmethod
    def setUpClass(cls):
        cls.pr = cProfile.Profile()
        cls.pr.enable()
        print('\nlxml')

    @classmethod
    def tearDownClass(cls):
        cls.pr.disable()
        Stats(cls.pr).strip_dirs().sort_stats('cumulative').print_stats(0)

    def test_init(self):
        self.assertIsInstance(exporter, HTML)


if __name__ == "__main__":
    unittest.main()
