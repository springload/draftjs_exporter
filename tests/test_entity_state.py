import unittest

from draftjs_exporter.command import Command
from draftjs_exporter.dom import DOM
from draftjs_exporter.entity_state import EntityException, EntityState
from draftjs_exporter.options import Options
from tests.test_entities import link

entity_decorators = {"LINK": link}

entity_map = {
    "0": {
        "type": "LINK",
        "mutability": "MUTABLE",
        "data": {"url": "http://example.com"},
    },
    "2": {"type": "LINK", "data": {"url": "http://test.com"}},
}


class TestEntityState(unittest.TestCase):
    def setUp(self):
        self.entity_state = EntityState(
            Options.map_entities(entity_decorators), entity_map
        )

    def test_init(self):
        self.assertIsInstance(self.entity_state, EntityState)

    def test_apply_start_entity(self):
        self.assertEqual(len(self.entity_state.entity_stack), 0)
        self.entity_state.apply(Command("start_entity", 0, "0"))
        self.assertEqual(self.entity_state.entity_stack[-1], "0")

    def test_apply_stop_entity(self):
        self.assertEqual(len(self.entity_state.entity_stack), 0)
        self.entity_state.apply(Command("start_entity", 0, "0"))
        self.entity_state.apply(Command("stop_entity", 5, "0"))
        self.assertEqual(len(self.entity_state.entity_stack), 0)

    def test_apply_raises(self):
        with self.assertRaises(EntityException):
            self.entity_state.apply(Command("start_entity", 0, "0"))
            self.entity_state.apply(Command("stop_entity", 0, "1"))

    def test_has_no_entity_default(self):
        self.assertEqual(self.entity_state.has_no_entity(), True)

    def test_has_no_entity_styled(self):
        self.entity_state.apply(Command("start_entity", 0, "0"))
        self.assertEqual(self.entity_state.has_no_entity(), False)

    def test_get_entity_details(self):
        self.assertEqual(
            self.entity_state.get_entity_details("0"),
            {
                "data": {"url": "http://example.com"},
                "type": "LINK",
                "mutability": "MUTABLE",
            },
        )

    def test_get_entity_details_raises(self):
        with self.assertRaises(EntityException):
            self.entity_state.get_entity_details("1")

    def test_render_entities_unstyled(self):
        self.assertEqual(
            self.entity_state.render_entities("Test text", {}, []), "Test text"
        )

    def test_render_entities_unicode(self):
        self.assertEqual(self.entity_state.render_entities("🍺", {}, []), "🍺")

    def test_render_entities_inline(self):
        self.entity_state.apply(Command("start_entity", 0, "0"))
        self.entity_state.render_entities("Test text", {}, [])
        self.entity_state.apply(Command("stop_entity", 9, "0"))
        self.assertEqual(
            DOM.render_debug(
                self.entity_state.render_entities("Test text", {}, [])
            ),
            '<a href="http://example.com">Test text</a>',
        )

    def test_render_entities_inline_multiple(self):
        self.entity_state.apply(Command("start_entity", 0, "0"))
        self.entity_state.render_entities("Test 1", {}, [])
        self.entity_state.apply(Command("stop_entity", 5, "0"))
        self.entity_state.apply(Command("start_entity", 5, "2"))
        self.assertEqual(
            DOM.render_debug(
                self.entity_state.render_entities("Test text", {}, [])
            ),
            '<a href="http://example.com">Test 1</a>',
        )
        self.entity_state.render_entities("Test 2", {}, [])
        self.entity_state.apply(Command("stop_entity", 10, "2"))
        self.assertEqual(
            DOM.render_debug(
                self.entity_state.render_entities("Test text", {}, [])
            ),
            '<a href="http://test.com"><fragment>Test textTest 2</fragment></a>',
        )

    def test_render_entities_data(self):
        blocks = [
            {
                "key": "5s7g9",
                "text": "test",
                "type": "unstyled",
                "depth": 0,
                "inlineStyleRanges": [],
                "entityRanges": [],
            }
        ]

        def component(props):
            self.assertEqual(props["entity"]["blocks"], blocks)
            self.assertEqual(props["entity"]["block"], blocks[0])
            self.assertEqual(props["entity"]["type"], "LINK")
            self.assertEqual(props["entity"]["mutability"], "MUTABLE")
            self.assertEqual(props["entity"]["entity_range"]["key"], "0")
            return None

        entity_state = EntityState(
            Options.map_entities({"LINK": component}), entity_map
        )

        entity_state.apply(Command("start_entity", 0, "0"))
        entity_state.render_entities("Test text", blocks[0], blocks)
        entity_state.apply(Command("stop_entity", 9, "0"))
        entity_state.render_entities("Test text", blocks[0], blocks)

    def test_render_entities_data_no_mutability(self):
        def component(props):
            self.assertEqual(props["entity"]["mutability"], None)
            return None

        entity_state = EntityState(
            Options.map_entities({"LINK": component}), entity_map
        )

        entity_state.apply(Command("start_entity", 0, "2"))
        entity_state.render_entities("Test text", {}, [])
        entity_state.apply(Command("stop_entity", 9, "2"))
        entity_state.render_entities("Test text", {}, [])
