import unittest

from draftjs_exporter.command import Command


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.command = Command('abracadabra', 5, 'shazam')

    def test_init(self):
        self.assertIsInstance(self.command, Command)

    def test_str(self):
        self.assertEqual(str(self.command), '<Command abracadabra 5 shazam>')


    def test_from_style_ranges_empty(self):
        self.assertEqual(str(Command.from_style_ranges({'inlineStyleRanges': []})), str([]))

    def test_from_style_ranges_single(self):
        self.assertEqual(str(Command.from_style_ranges({
            'inlineStyleRanges': [
                {
                    'offset': 0,
                    'length': 4,
                    'style': 'shazam',
                }
            ]
        })), str([
            Command('start_inline_style', 0, 'shazam'),
            Command('stop_inline_style', 4, 'shazam'),
        ]))

    def test_from_style_ranges_multiple(self):
        self.assertEqual(str(Command.from_style_ranges({
            'inlineStyleRanges': [
                {
                    'offset': 0,
                    'length': 4,
                    'style': 'shazam',
                },
                {
                    'offset': 9,
                    'length': 3,
                    'style': 'wazzum',
                },
            ],
        })), str([
            Command('start_inline_style', 0, 'shazam'),
            Command('stop_inline_style', 4, 'shazam'),
            Command('start_inline_style', 9, 'wazzum'),
            Command('stop_inline_style', 12, 'wazzum'),
        ]))

    def test_from_entity_ranges_multiple(self):
        self.assertEqual(str(Command.from_entity_ranges({
            'entityRanges': [
                {
                    'offset': 0,
                    'length': 4,
                    'key': 3,
                },
                {
                    'offset': 9,
                    'length': 3,
                    'key': 10,
                },
            ],
        })), str([
            Command('start_entity', 0, '3'),
            Command('stop_entity', 4, '3'),
            Command('start_entity', 9, '10'),
            Command('stop_entity', 12, '10'),
        ]))
