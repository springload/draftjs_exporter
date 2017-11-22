# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import cProfile
import logging
import os
from pstats import Stats
from memory_profiler import profile

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML

from markov_draftjs import get_content_sample

from example import ListItem, OrderedList, Image, BR, EntityFallback


def Document(props):
    return DOM.create_element('a', {
        'title': props.get('label'),
        'href': '/documents/%s' % props.get('id'),
    }, props['children'])


def Link(props):
    return DOM.create_element('a', {
        'href': props['url'],
    }, props['children'])


def BlockFallback(props):
    type_ = props['block']['type']

    logging.warn('Missing config for "%s".' % type_)
    return DOM.create_element('div', {}, props['children'])


config = {
    'block_map': dict(BLOCK_MAP, **{
        BLOCK_TYPES.HEADER_TWO: 'h2',
        BLOCK_TYPES.HEADER_THREE: {'element': 'h3', 'props': {'class': 'u-text-center'}},
        BLOCK_TYPES.UNORDERED_LIST_ITEM: {
            'element': 'li',
            'wrapper': 'ul',
            'wrapper_props': {'class': 'bullet-list'},
        },
        BLOCK_TYPES.ORDERED_LIST_ITEM: {
            'element': ListItem,
            'wrapper': OrderedList,
        },
        BLOCK_TYPES.FALLBACK: BlockFallback
    }),
    'style_map': STYLE_MAP,
    'entity_decorators': {
        ENTITY_TYPES.IMAGE: Image,
        ENTITY_TYPES.LINK: Link,
        ENTITY_TYPES.DOCUMENT: Document,
        ENTITY_TYPES.HORIZONTAL_RULE: lambda props: DOM.create_element('hr'),
        ENTITY_TYPES.EMBED: None,
        ENTITY_TYPES.FALLBACK: EntityFallback,
    },
    'composite_decorators': [
        BR,
    ],
    'engine': 'string',
}

exporter = HTML(config)

content_states = get_content_sample()

BENCHMARK_RUNS = int(os.environ.get('BENCHMARK_RUNS', 1))

print('Exporting %s ContentStates %s times' %
      (len(content_states), BENCHMARK_RUNS))

pr = cProfile.Profile()
pr.enable()

for i in range(0, BENCHMARK_RUNS):
    for content_state in content_states:
        exporter.render(content_state)

pr.disable()
p = Stats(pr)

p.strip_dirs().sort_stats('cumulative').print_stats(10)

print('Measuring memory consumption')


@profile(precision=6)
def memory_consumption_run():
    exporter = HTML(config)

    for content_state in content_states:
        exporter.render(content_state)


memory_consumption_run()
