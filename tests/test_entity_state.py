import unittest

from draft_exporter.entities.link import Link
from draft_exporter.entity_state import EntityState

entity_decorators = {
    'LINK': Link
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
        self.entity_state = EntityState('todo', entity_decorators, entity_map)

    def test_init(self):
        self.assertIsInstance(self.entity_state, EntityState)

    @unittest.skip('TODO')
    def test_apply_start_entity(self):
        self.assertEquals(self.entity_state.entity_stack, [])
        self.entity_state.apply({'name': 'start_entity', 'data': {}})
        self.assertEquals(self.entity_state.entity_stack, [])

    @unittest.skip('TODO')
    def test_apply_stop_entity(self):
        self.assertEquals(self.entity_state.entity_stack, [])
        self.entity_state.apply({'name': 'stop_entity', 'data': {}})
        self.assertEquals(self.entity_state.entity_stack, [])
