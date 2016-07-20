from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.entities.null import Null


class TestNull(unittest.TestCase):
    def setUp(self):
        self.null = Null()

    def test_init(self):
        self.assertIsInstance(self.null, Null)

    def test_render(self):
        self.assertEqual(DOM.get_tag_name(self.null.render({})), 'fragment')
        self.assertEqual(DOM.get_text_content(self.null.render({})), None)
