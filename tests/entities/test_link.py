import unittest
from draft_exporter.entities.link import Link


class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Link()

    def test_init(self):
        self.assertIsInstance(self.link, Link)

    @unittest.skip('TODO')
    def test_call(self):
        self.assertEqual(self.link.call({'test': 5}), {'test': 5})
