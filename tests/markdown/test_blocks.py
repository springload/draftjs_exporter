import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.blocks import list_wrapper, ol, prefixed_block, ul


class TestBlocks(unittest.TestCase):
    def test_prefixed_block(self):
        self.assertEqual(
            DOM.render(prefixed_block("> ")({"children": "test"})), "> test\n\n"
        )

    def test_ul(self):
        self.assertEqual(
            DOM.render(
                ul(
                    {
                        "block": {
                            "depth": 0,
                        },
                        "children": "test",
                    }
                )
            ),
            "* test\n",
        )

    def test_ol(self):
        b = {
            "key": "a",
            "type": "ordered-list-item",
            "depth": 0,
        }
        self.assertEqual(
            DOM.render(
                ol(
                    {
                        "block": b,
                        "blocks": [b],
                        "children": "test",
                    }
                )
            ),
            "1. test\n\n",
        )

    def test_ol_numbering(self):
        b = {
            "key": "a",
            "type": "ordered-list-item",
            "depth": 0,
        }
        self.assertEqual(
            DOM.render(
                ol(
                    {
                        "block": b,
                        "blocks": [
                            dict(b, **{"key": "b"}),
                            b,
                        ],
                        "children": "test",
                    }
                )
            ),
            "2. test\n\n",
        )

    def test_list_wrapper(self):
        self.assertEqual(DOM.render(list_wrapper({})), "")
