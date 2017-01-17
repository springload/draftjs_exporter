# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import cProfile
import json
import os
from pstats import Stats

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.defaults import BLOCK_MAP
from draftjs_exporter.html import HTML
from tests.test_entities import Image, Link

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
    }),
    'style_map': {
        INLINE_STYLES.ITALIC: {'element': 'em'},
        INLINE_STYLES.BOLD: {'element': 'strong'},
    },
}

fixtures_path = os.path.join(os.path.dirname(__file__), 'tests', 'test_exports.json')
fixtures = json.loads(open(fixtures_path, 'r').read())

exporter = HTML(config)

pr = cProfile.Profile()
pr.enable()

# Run profiling on the test fixtures.
for export in fixtures:
    HTML(config).render(export.get('content_state'))

pr.disable()

p = Stats(pr)
p.strip_dirs().sort_stats('cumulative').print_stats(20)
