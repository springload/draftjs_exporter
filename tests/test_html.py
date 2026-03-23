import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed

from draftjs_exporter.command import Command
from draftjs_exporter.dom import DOM
from draftjs_exporter.html import HTML, ExporterConfig
from draftjs_exporter.types import ContentState

config: ExporterConfig = {
    "entity_decorators": {},
    "block_map": {
        "header-one": {"element": "h1"},
        "unordered-list-item": {
            "element": "li",
            "wrapper": "ul",
        },
        "unstyled": {"element": "p"},
    },
    "style_map": {"ITALIC": {"element": "em"}, "BOLD": {"element": "strong"}},
}


class TestHTML(unittest.TestCase):
    def setUp(self):
        self.exporter = HTML(config)

    def test_init(self):
        self.assertIsInstance(self.exporter, HTML)

    def test_init_dom_engine_default(self):
        exporter = HTML()
        self.assertEqual(exporter._engine, DOM.STRING)

    def test_render_block_exists(self):
        self.assertTrue("render_block" in dir(self.exporter))

    def test_build_commands_empty(self):
        self.assertEqual(
            str(
                self.exporter.build_commands(
                    {
                        "key": "dem5p",
                        "text": "some paragraph text",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [],
                        "entityRanges": [],
                    }
                )
            ),
            str([Command("start_text", 0), Command("stop_text", 19)]),
        )

    def test_build_commands_multiple(self):
        self.assertEqual(
            str(
                self.exporter.build_commands(
                    {
                        "key": "dem5p",
                        "text": "some paragraph text",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [
                            {"offset": 0, "length": 4, "style": "ITALIC"},
                            {"offset": 9, "length": 3, "style": "BOLD"},
                        ],
                        "entityRanges": [
                            {"offset": 5, "length": 9, "key": 0},
                            {"offset": 0, "length": 4, "key": 1},
                        ],
                    }
                )
            ),
            str(
                [
                    Command("start_text", 0),
                    Command("start_inline_style", 0, "ITALIC"),
                    Command("start_entity", 0, "1"),
                    Command("stop_inline_style", 4, "ITALIC"),
                    Command("stop_entity", 4, "1"),
                    Command("start_entity", 5, "0"),
                    Command("start_inline_style", 9, "BOLD"),
                    Command("stop_inline_style", 12, "BOLD"),
                    Command("stop_entity", 14, "0"),
                    Command("stop_text", 19),
                ]
            ),
        )

    def test_build_command_groups_empty(self):
        self.assertEqual(
            str(
                self.exporter.build_command_groups(
                    {
                        "key": "dem5p",
                        "text": "some paragraph text",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [],
                        "entityRanges": [],
                    }
                )
            ),
            str(
                [
                    ("some paragraph text", [Command("start_text", 0)]),
                    ("", [Command("stop_text", 19)]),
                ]
            ),
        )

    def test_build_command_groups_multiple(self):
        self.assertEqual(
            str(
                self.exporter.build_command_groups(
                    {
                        "key": "dem5p",
                        "text": "some paragraph text",
                        "type": "unstyled",
                        "depth": 0,
                        "inlineStyleRanges": [
                            {"offset": 0, "length": 4, "style": "ITALIC"},
                            {"offset": 9, "length": 3, "style": "BOLD"},
                        ],
                        "entityRanges": [
                            {"offset": 5, "length": 9, "key": 0},
                            {"offset": 0, "length": 4, "key": 1},
                        ],
                    }
                )
            ),
            str(
                [
                    (
                        "some",
                        [
                            Command("start_text", 0),
                            Command("start_inline_style", 0, "ITALIC"),
                            Command("start_entity", 0, "1"),
                        ],
                    ),
                    (
                        " ",
                        [
                            Command("stop_inline_style", 4, "ITALIC"),
                            Command("stop_entity", 4, "1"),
                        ],
                    ),
                    ("para", [Command("start_entity", 5, "0")]),
                    ("gra", [Command("start_inline_style", 9, "BOLD")]),
                    ("ph", [Command("stop_inline_style", 12, "BOLD")]),
                    (" text", [Command("stop_entity", 14, "0")]),
                    ("", [Command("stop_text", 19)]),
                ]
            ),
        )

    def test_render(self):
        self.assertEqual(
            self.exporter.render(
                {
                    "entityMap": {},
                    "blocks": [
                        {
                            "key": "5s7g9",
                            "text": "Header",
                            "type": "header-one",
                            "depth": 0,
                            "inlineStyleRanges": [],
                            "entityRanges": [],
                        }
                    ],
                }
            ),
            "<h1>Header</h1>",
        )

    def test_render_block_defaults(self):
        self.assertEqual(
            self.exporter.render({"entityMap": {}, "blocks": [{"text": "Paragraph"}]}),
            "<p>Paragraph</p>",
        )

    def test_render_empty(self):
        self.assertEqual(self.exporter.render({"entityMap": {}, "blocks": []}), "")

    def test_render_none(self):
        self.assertEqual(self.exporter.render(None), "")

    def test_render_twice(self):
        """Asserts no state is kept during renders."""
        self.assertEqual(
            self.exporter.render(
                {
                    "entityMap": {},
                    "blocks": [
                        {
                            "key": "5s7g9",
                            "text": "Header",
                            "type": "header-one",
                            "depth": 0,
                            "inlineStyleRanges": [],
                            "entityRanges": [],
                        }
                    ],
                }
            ),
            "<h1>Header</h1>",
        )
        self.assertEqual(
            self.exporter.render(
                {
                    "entityMap": {},
                    "blocks": [
                        {
                            "key": "5s7g9",
                            "text": "Header",
                            "type": "header-one",
                            "depth": 0,
                            "inlineStyleRanges": [],
                            "entityRanges": [],
                        }
                    ],
                }
            ),
            "<h1>Header</h1>",
        )

    def test_engine_is_per_instance(self):
        """Each HTML instance uses its own engine, unaffected by other instances."""
        html_string = HTML({"engine": DOM.STRING})
        HTML({"engine": DOM.STRING_COMPAT})

        # html_string still uses STRING even though STRING_COMPAT was created after.
        self.assertEqual(
            html_string.render({"entityMap": {}, "blocks": [{"text": 'Quote "here"'}]}),
            '<p>Quote "here"</p>',
        )

    def test_engine_isolation_between_instances(self):
        """Each HTML instance uses its own engine, unaffected by other instances."""
        html_compat = HTML({"engine": DOM.STRING_COMPAT})
        HTML({"engine": DOM.STRING})

        # html_compat still uses STRING_COMPAT even though STRING was created after.
        self.assertEqual(
            html_compat.render({"entityMap": {}, "blocks": [{"text": 'Quote "here"'}]}),
            "<p>Quote &quot;here&quot;</p>",
        )

    def test_render_concurrent_different_engines(self):
        """Two exporters with different engines render correctly in parallel."""
        content_state: ContentState = {
            "entityMap": {},
            "blocks": [{"text": 'Quote "here"'}],
        }

        html_string = HTML({"engine": DOM.STRING})
        html_compat = HTML({"engine": DOM.STRING_COMPAT})

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {
                pool.submit(html_string.render, content_state): "string",
                pool.submit(html_compat.render, content_state): "string_compat",
            }

            results = {}
            for future in as_completed(futures):
                results[futures[future]] = future.result()

        self.assertEqual(results["string"], '<p>Quote "here"</p>')
        self.assertEqual(results["string_compat"], "<p>Quote &quot;here&quot;</p>")

    def test_render_concurrent_same_engine(self):
        """Multiple renders of the same exporter work correctly in parallel."""
        exporter = HTML(config)
        content_states: list[ContentState] = []
        for i in range(10):
            content_states.append({"entityMap": {}, "blocks": [{"text": f"Block {i}"}]})

        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(exporter.render, cs) for cs in content_states]
            results = [f.result() for f in futures]

        for i, result in enumerate(results):
            self.assertEqual(result, f"<p>Block {i}</p>")
