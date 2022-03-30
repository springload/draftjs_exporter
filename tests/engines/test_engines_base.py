import unittest

from draftjs_exporter.engines.base import DOMEngine


class TestDOMEngine(unittest.TestCase):
    def test_create_tag(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.create_tag("tag")

    def test_parse_html(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.parse_html("html")

    def test_append_child(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.append_child(None, None)

    def test_render(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.render(None)

    def test_render_debug(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.render_debug(None)
