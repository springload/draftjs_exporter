from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from tests.test_entities import Icon


class TestDOM(unittest.TestCase):
    def test_create_element(self):
        self.assertEqual(DOM.render(DOM.create_element('p', {'className': 'intro'}, 'Test test')), '<p class="intro">Test test</p>')

    def test_create_element_style_dict(self):
        self.assertEqual(DOM.render(DOM.create_element('p', {'style': {'borderColor': 'red', 'textDecoration': 'underline'}}, 'Test test')), '<p style="border-color: red;text-decoration: underline;">Test test</p>')

    def test_create_element_style_str(self):
        self.assertEqual(DOM.render(DOM.create_element('p', {'style': 'border-color: red;text-decoration: underline;'}, 'Test test')), '<p style="border-color: red;text-decoration: underline;">Test test</p>')

    def test_create_element_empty(self):
        self.assertEqual(DOM.render_debug(DOM.create_element()), '<fragment></fragment>')

    def test_create_element_nested(self):
        self.assertEqual(DOM.render_debug(DOM.create_element('a', {}, DOM.create_element('span', {'className': 'file-info icon-text'}, DOM.create_element('span', {'className': 'icon-text__text'}, 'Test test'), DOM.create_element('svg', {'className': 'icon'}, DOM.create_element('use', {'xlink:href': '#icon-test'}))))), '<a><span class="file-info icon-text"><span class="icon-text__text">Test test</span><svg class="icon"><use xlink:href="#icon-test"></use></svg></span></a>')

    def test_create_element_none(self):
        self.assertEqual(DOM.render_debug(DOM.create_element('a', {}, None, DOM.create_element('span', {}, 'Test test'))), '<a><span>Test test</span></a>')

    def test_create_element_entity(self):
        self.assertEqual(DOM.render_debug(DOM.create_element(Icon, {'name': 'rocket'})), '<svg class="icon"><use xlink:href="#icon-rocket"></use></svg>')

    def test_create_element_entity_configured(self):
        self.assertEqual(DOM.render_debug(DOM.create_element(Icon(icon_class='i'), {'name': 'rocket'})), '<svg class="i"><use xlink:href="#icon-rocket"></use></svg>')

    def test_parse_html(self):
        self.assertEqual(DOM.render_debug(DOM.parse_html('<p><span>Test text</span></p>')), '<p><span>Test text</span></p>')

    def test_camel_to_dash(self):
        self.assertEqual(DOM.camel_to_dash('testCamelToDash'), 'test-camel-to-dash')
        self.assertEqual(DOM.camel_to_dash('TestCamelToDash'), 'test-camel-to-dash')
        self.assertEqual(DOM.camel_to_dash('TestCamelTODash'), 'test-camel-to-dash')
        self.assertEqual(DOM.camel_to_dash('TestCamelTODasH'), 'test-camel-to-das-h')
        self.assertEqual(DOM.camel_to_dash('testcameltodash'), 'testcameltodash')
        self.assertEqual(DOM.camel_to_dash('test-Camel-ToDash'), 'test-camel-to-dash')

    def test_append_child(self):
        parent = DOM.create_element('p')
        DOM.append_child(parent, DOM.create_element('span', {}, 'Test text'))
        self.assertEqual(DOM.render_debug(parent), '<p><span>Test text</span></p>')

    def test_get_children(self):
        self.assertEqual(len(DOM.get_children(DOM.create_element('span', {}, DOM.create_element('span'), DOM.create_element('span')))), 2)

    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element('a', {}, DOM.create_element('span', {'className': 'file-info icon-text'}, DOM.create_element('span', {'className': 'icon-text__text'}, 'Test test'), DOM.create_element('svg', {'className': 'icon'}, DOM.create_element('use', {'xlink:href': '#icon-test'}))))), '<a><span class="file-info icon-text"><span class="icon-text__text">Test test</span><svg class="icon"><use xlink:href="#icon-test"></use></svg></span></a>')

    def test_pretty_print(self):
        self.assertEqual(DOM.pretty_print('<a><span class="file-info icon-text"><span class="icon-text__text">Test test</span><svg class="icon"><use xlink:href="#icon-test"></use></svg></span></a>'), '<a>\n   <span class="file-info icon-text">\n    <span class="icon-text__text">\n     Test test\n    </span>\n    <svg class="icon">\n     <use xlink:href="#icon-test">\n     </use>\n    </svg>\n   </span>\n  </a>')
