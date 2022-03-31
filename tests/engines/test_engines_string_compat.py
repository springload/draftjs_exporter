import unittest

from draftjs_exporter.engines.string_compat import DOMStringCompat

S = DOMStringCompat


class TestDOMStringCompat(unittest.TestCase):
    def test_create_tag(self):
        self.assertEqual(
            S.render_debug(S.create_tag("p", {"class": "intro"})),
            '<p class="intro"></p>',
        )

    def test_create_tag_empty(self):
        self.assertEqual(S.render_debug(S.create_tag("p")), "<p></p>")

    def test_parse_html(self):
        self.assertEqual(
            S.render(S.parse_html("<p><span>Test text</span></p>")),
            "<p><span>Test text</span></p>",
        )
        # There for test coverage only.
        self.assertEqual(
            S.render_debug(S.parse_html("<p><span>Test text</span></p>")),
            "<p><span>Test text</span></p>",
        )

    def test_append_child(self):
        parent = S.create_tag("p")
        S.append_child(parent, S.create_tag("span", {}))
        self.assertEqual(S.render_debug(parent), "<p><span></span></p>")

    def test_append_child_identical_text(self):
        parent = S.create_tag("p")
        S.append_child(parent, S.parse_html("test"))
        S.append_child(parent, S.parse_html("test"))
        self.assertEqual(S.render_debug(parent), "<p>testtest</p>")

    def test_append_child_identical_elements(self):
        parent = S.create_tag("p")
        S.append_child(parent, S.create_tag("br"))
        S.append_child(parent, S.create_tag("br"))
        self.assertEqual(S.render_debug(parent), "<p><br/><br/></p>")

    def test_render_attrs_escaping(self):
        self.assertEqual(
            S.render_attrs(
                {"alt": "img's alt", "class": 'intro " text', "src": "src.png"}
            ),
            ' alt="img&#x27;s alt" class="intro &quot; text" src="src.png"',
        )

    def test_render_attrs_sorting(self):
        self.assertEqual(
            S.render_attrs(
                {
                    "class": 'intro " text',
                    "src": "src.png",
                    "alt": "img's alt",
                }
            ),
            ' alt="img&#x27;s alt" class="intro &quot; text" src="src.png"',
        )

    def test_render_children(self):
        self.assertEqual(
            S.render_children(
                [
                    "single ' quote",
                    S.create_tag("p", {"class": "intro"}),
                    'double " quote',
                ]
            ),
            'single &#x27; quote<p class="intro"></p>double &quot; quote',
        )

    def test_render(self):
        self.assertEqual(
            S.render_debug(S.create_tag("p", {"class": "intro"})),
            '<p class="intro"></p>',
        )

    def test_render_debug(self):
        self.assertEqual(
            S.render_debug(S.create_tag("p", {"class": "intro"})),
            '<p class="intro"></p>',
        )
        # There for test coverage only.
        self.assertEqual(
            S.render_debug(S.create_tag("img", {"class": "intro"})),
            '<img class="intro"/>',
        )
