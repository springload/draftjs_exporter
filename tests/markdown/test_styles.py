import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.styles import inline_style


class TestInlineStyle(unittest.TestCase):
    def test_works(self):
        self.assertEqual(DOM.render(inline_style("*")({"children": "test"})), "*test*")
