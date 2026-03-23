import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.helpers import block, inline


class TestHelpers(unittest.TestCase):
    def test_inline(self):
        self.assertEqual(DOM.render(inline(["test"])), "test")

    def test_block(self):
        self.assertEqual(DOM.render(block(["test"])), "test\n\n")
