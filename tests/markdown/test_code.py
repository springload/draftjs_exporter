import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.markdown.code import (
    code_element,
    code_wrapper,
    make_code_element,
    make_code_wrapper,
)


class TestCodeElement(unittest.TestCase):
    def test_works(self):
        self.assertEqual(
            DOM.render(
                code_element(
                    {
                        "block": {},
                        "children": "test",
                    }
                )
            ),
            "test\n",
        )

    def test_block_end(self):
        b = {
            "key": "a",
            "type": "code-block",
            "text": "test",
            "depth": 0,
        }
        self.assertEqual(
            DOM.render(
                code_element(
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
            "test\n```\n\n",
        )


class TestMakeCodeElement(unittest.TestCase):
    def test_tilde_fence(self):
        self.assertEqual(
            DOM.render(
                make_code_element("~~~")(
                    {
                        "block": {},
                        "children": "test",
                    }
                )
            ),
            "test\n",
        )

    def test_tilde_fence_block_end(self):
        b = {
            "key": "a",
            "type": "code-block",
            "text": "test",
            "depth": 0,
        }
        self.assertEqual(
            DOM.render(
                make_code_element("~~~")(
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
            "test\n~~~\n\n",
        )


class TestCodeWrapper(unittest.TestCase):
    def test_works(self):
        self.assertEqual(
            DOM.render(
                code_wrapper(
                    {
                        "block": {},
                        "children": "test",
                    }
                )
            ),
            "```\n",
        )


class TestMakeCodeWrapper(unittest.TestCase):
    def test_tilde_fence(self):
        self.assertEqual(
            DOM.render(
                make_code_wrapper("~~~")(
                    {
                        "block": {},
                        "children": "test",
                    }
                )
            ),
            "~~~\n",
        )
