import unittest
from draft_exporter.entities.null import Null


class TestNull(unittest.TestCase):
    def setUp(self):
        self.null = Null()

    def test_init(self):
        self.assertIsInstance(self.null, Null)

    def test_call(self):
        self.assertEquals(self.null.call({'test': 5}), {'test': 5})
