import unittest
from draft_exporter.style_state import StyleState

style_map = {
    'ITALIC': {'fontStyle': 'italic'},
    'BOLD': {'fontStyle': 'bold'}
}


class TestStyleState(unittest.TestCase):
    def setUp(self):
        self.style_state = StyleState(style_map)

    def test_init(self):
        self.assertIsInstance(self.style_state, StyleState)

    @unittest.skip('TODO')
    def test_apply_start_inline_style(self):
        self.assertEquals(self.style_state.styles, [])
        self.style_state.apply({'name': 'start_inline_style', 'data': {}})
        self.assertEquals(self.style_state.styles, [])

    @unittest.skip('TODO')
    def test_apply_stop_inline_style(self):
        self.assertEquals(self.style_state.styles, [])
        self.style_state.apply({'name': 'stop_inline_style', 'data': {}})
        self.assertEquals(self.style_state.styles, [])
