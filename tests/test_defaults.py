from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP, CodeBlock, render_children
from draftjs_exporter.dom import DOM


class TestDefaults(unittest.TestCase):
    def test_default_block_map(self):
        self.assertIsInstance(BLOCK_MAP, object)

    def test_default_style_map(self):
        self.assertIsInstance(STYLE_MAP, object)

    def test_render_children(self):
        self.assertEqual(render_children({'children': 'test'}), 'test')


class TestCodeBlock(unittest.TestCase):
    def test_render(self):
        self.assertEqual(DOM.render_debug(CodeBlock({'children': 'test'})), '<pre><code>test</code></pre>')
