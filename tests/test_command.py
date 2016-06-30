import unittest
from draft_exporter.command import Command


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.command = Command('abracadabra', 5, 'shazam')

    def test_init(self):
        self.assertIsInstance(self.command, Command)

    def test_call(self):
        self.assertEquals(str(self.command), '<Command abracadabra 5 shazam>')
