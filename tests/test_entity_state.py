from __future__ import absolute_import, unicode_literals

import unittest

from lxml import etree

from draftjs_exporter.command import Command
from draftjs_exporter.entities.link import Link
from draftjs_exporter.entity_state import EntityException, EntityState

entity_decorators = {
    'LINK': Link()
}

entity_map = {
    '0': {
        'type': 'LINK',
        'mutability': 'MUTABLE',
        'data': {
            'url': 'http://example.com'
        }
    }
}


class TestEntityState(unittest.TestCase):
    def setUp(self):
        self.entity_state = EntityState(etree.Element('div'), entity_decorators, entity_map)

    def test_init(self):
        self.assertIsInstance(self.entity_state, EntityState)

    @unittest.skip('TODO')
    def test_apply_start_entity(self):
        self.assertEqual(self.entity_state.entity_stack[-1][0].tag, 'div')
        self.assertEqual(self.entity_state.entity_stack[-1][1], {})
        self.entity_state.apply(Command('start_entity', 0, 0))
        self.assertEqual(self.entity_state.entity_stack[-1], {
            'data': {
                'url': 'http://example.com'
            },
            'type': 'LINK',
            'mutability': 'MUTABLE',
        })

    @unittest.skip('TODO')
    def test_apply_stop_entity(self):
        self.assertEqual(self.entity_state.entity_stack[-1][0].tag, 'div')
        self.assertEqual(self.entity_state.entity_stack[-1][1], {})
        self.entity_state.apply(Command('stop_entity', 5, 0))
        self.assertEqual(self.entity_state.entity_stack[-1][1], {
            'data': {
                'url': 'http://example.com'
            },
            'type': 'LINK',
            'mutability': 'MUTABLE',
        })

    def test_start_command_raises(self):
        with self.assertRaises(EntityException):
            self.entity_state.start_command(Command('start_entity', 0, 1))

    def test_stop_command_raises(self):
        with self.assertRaises(EntityException):
            self.entity_state.start_command(Command('stop_entity', 0, 1))
