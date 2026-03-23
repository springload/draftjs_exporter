import unittest

import draftjs_exporter
from draftjs_exporter import (
    BLOCK_TYPES,
    DOM,
    HTML,
    HTML_CONFIG,
    MARKDOWN_CONFIG,
    ContentState,
    Exporter,
    ExporterConfig,
)


class TestTopLevelAPI(unittest.TestCase):
    def test_exporter_is_html(self):
        self.assertIs(Exporter, HTML)

    def test_all_members_importable(self):
        for name in draftjs_exporter.__all__:
            self.assertTrue(hasattr(draftjs_exporter, name), f"{name} not importable")

    def test_html_config_keys(self):
        self.assertIn("block_map", HTML_CONFIG)
        self.assertIn("style_map", HTML_CONFIG)
        self.assertIn("engine", HTML_CONFIG)

    def test_html_config_engine(self):
        self.assertEqual(HTML_CONFIG["engine"], DOM.STRING)

    def test_markdown_config_keys(self):
        self.assertIn("block_map", MARKDOWN_CONFIG)
        self.assertIn("style_map", MARKDOWN_CONFIG)
        self.assertIn("entity_decorators", MARKDOWN_CONFIG)
        self.assertIn("engine", MARKDOWN_CONFIG)

    def test_markdown_config_engine(self):
        self.assertEqual(MARKDOWN_CONFIG["engine"], DOM.MARKDOWN)


content_state: ContentState = {
    "entityMap": {},
    "blocks": [
        {
            "key": "a",
            "text": "Hello, World!",
            "type": "unstyled",
            "depth": 0,
            "inlineStyleRanges": [],
            "entityRanges": [],
        },
    ],
}


class TestExporterRendering(unittest.TestCase):
    def test_html_config_matches_default(self):
        """HTML_CONFIG should produce the same output as HTML() with no config."""
        default = HTML().render(content_state)
        explicit = Exporter(HTML_CONFIG).render(content_state)
        self.assertEqual(default, explicit)

    def test_html_config_render(self):
        result = Exporter(HTML_CONFIG).render(content_state)
        self.assertEqual(result, "<p>Hello, World!</p>")

    def test_markdown_config_render(self):
        result = Exporter(MARKDOWN_CONFIG).render(content_state)
        self.assertEqual(result, "Hello, World!\n\n")

    def test_html_config_extend(self):
        """Spreading HTML_CONFIG with overrides should work."""
        config: ExporterConfig = {
            **HTML_CONFIG,
            "block_map": {
                **HTML_CONFIG["block_map"],
                BLOCK_TYPES.UNSTYLED: "div",
            },
        }
        result = Exporter(config).render(content_state)
        self.assertEqual(result, "<div>Hello, World!</div>")
