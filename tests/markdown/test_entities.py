import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.entities import horizontal_rule, image, link


class TestEntities(unittest.TestCase):
    def test_horizontal_rule(self):
        self.assertEqual(DOM.render(horizontal_rule({})), "---\n\n")

    def test_image(self):
        self.assertEqual(
            DOM.render(image({"src": "test.png"})),
            "![](test.png)\n\n",
        )

    def test_image_alt(self):
        self.assertEqual(
            DOM.render(image({"src": "test.png", "alt": "test"})),
            "![test](test.png)\n\n",
        )

    def test_link(self):
        self.assertEqual(
            DOM.render(link({"url": "http://www.example.com/", "children": "test"})),
            "[test](http://www.example.com/)",
        )
