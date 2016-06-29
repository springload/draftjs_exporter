import unittest

from draft_exporter.entities.link import Link
from draft_exporter.html import HTML

config = {
    'entity_decorators': {
        'LINK': Link
    },
    'block_map': {
        'header-one': {'element': 'h1'},
        'unordered-list-item': {
            'element': 'li',
            'wrapper': ['ul', {'className': 'public-DraftStyleDefault-ul'}]
        },
        'unstyled': {'element': 'div'}
    },
    'style_map': {
        'ITALIC': {'fontStyle': 'italic'},
        'BOLD': {'fontStyle': 'bold'}
    }
}


# Initialised from https://github.com/ignitionworks/draftjs_exporter/blob/c4a92b303e9f9dbce20e224f66f3114d8a0807ff/spec/integrations/html_spec.rb
class TestHTML(unittest.TestCase):
    def setUp(self):
        self.exporter = HTML(config)

    def test_init(self):
        self.assertIsInstance(self.exporter, HTML)

    def test_call_returns_str(self):
        self.assertIsInstance(self.exporter.call({
            'entityMap': {},
            'blocks': [
                {
                    'key': '5s7g9',
                    'text': 'Header',
                    'type': 'header-one',
                    'depth': 0,
                    'inlineStyleRanges': [],
                    'entityRanges': []
                },
            ]
        }), str)

    @unittest.skip('TODO')
    def test_block_contents(self):
        # self.exporter.block_contents(self, element, block, entity_map)
        pass

    @unittest.skip('TODO')
    def test_add_node(self):
        # self.exporter.add_node(self, element, text, style_state)
        pass

    @unittest.skip('TODO')
    def test_build_command_groups(self):
        # self.exporter.build_command_groups(self, block)
        pass

    @unittest.skip('TODO')
    def test_build_commands(self):
        # self.exporter.build_commands(self, block)
        pass

    @unittest.skip('TODO')
    def test_build_range_commands(self):
        # self.exporter.build_range_commands(self, name, data_key, ranges)
        pass
