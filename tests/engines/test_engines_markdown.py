import unittest

from draftjs_exporter.engines.markdown import DOMMarkdown

M = DOMMarkdown


class TestDOMMarkdown(unittest.TestCase):
    def test_create_tag(self):
        self.assertEqual(
            M.render_debug(M.create_tag("p", {"class": "intro"})),
            '<p class="intro"></p>',
        )

    def test_create_tag_empty(self):
        self.assertEqual(M.render_debug(M.create_tag("p")), "<p></p>")

    def test_parse_html(self):
        self.assertEqual(
            M.render(M.parse_html("<p><span>Test text</span></p>")),
            "<p><span>Test text</span></p>",
        )

    def test_append_child(self):
        parent = M.create_tag("p")
        M.append_child(parent, M.create_tag("span", {}))
        self.assertEqual(M.render_debug(parent), "<p><span></span></p>")

    def test_append_child_identical_text(self):
        parent = M.create_tag("p")
        M.append_child(parent, "test")
        M.append_child(parent, "test")
        self.assertEqual(M.render_debug(parent), "<p>testtest</p>")

    def test_append_child_identical_elements(self):
        parent = M.create_tag("p")
        M.append_child(parent, M.create_tag("br"))
        M.append_child(parent, M.create_tag("br"))
        self.assertEqual(M.render_debug(parent), "<p><br/><br/></p>")

    def test_append_child_same_elements(self):
        elt = M.create_tag("br")
        parent = M.create_tag("p")
        M.append_child(parent, elt)
        M.append_child(parent, elt)
        self.assertEqual(M.render_debug(parent), "<p><br/></p>")

    def test_render_attrs(self):
        self.assertEqual(
            M.render_attrs(
                {
                    "src": "src.png",
                    "alt": "img's alt",
                    "class": "intro",
                }
            ),
            ' alt="img&#x27;s alt" class="intro" src="src.png"',
        )

    def test_render_children(self):
        self.assertEqual(
            M.render_children(
                [
                    "render children",
                    M.create_tag("p", {"class": "intro"}),
                    "test test",
                ]
            ),
            'render children<p class="intro"></p>test test',
        )

    def test_render_children_no_escaping(self):
        """Unlike DOMString, the Markdown engine does not escape text content."""
        self.assertEqual(
            M.render_children(["<strong>not escaped</strong>"]),
            "<strong>not escaped</strong>",
        )

    def test_render(self):
        self.assertEqual(
            M.render_debug(M.create_tag("p", {"class": "intro"})),
            '<p class="intro"></p>',
        )

    def test_render_debug(self):
        self.assertEqual(
            M.render_debug(M.create_tag("p", {"class": "intro"})),
            '<p class="intro"></p>',
        )
