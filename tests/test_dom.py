from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom import DOM
from draftjs_exporter.entities import Icon


class TestDOM(unittest.TestCase):
    def test_create_tag(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_tag('p', {'class': 'intro'})), 'p')
        self.assertEqual(DOM.get_class_list(DOM.create_tag('p', {'class': 'intro'})), ['intro'])
        self.assertEqual(DOM.get_text_content(DOM.create_tag('p', {'class': 'intro'})), None)

    def test_create_element(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_element('p', {'className': 'intro'}, 'Test test')), 'p')
        self.assertEqual(DOM.get_class_list(DOM.create_element('p', {'className': 'intro'}, 'Test test')), ['intro'])
        self.assertEqual(DOM.get_text_content(DOM.create_element('p', {'className': 'intro'}, 'Test test')), 'Test test')

    def test_create_element_empty(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_element()), 'fragment')

    def test_create_element_nested(self):
        self.assertEqual(DOM.render(DOM.create_element('a', {}, DOM.create_element('span', {'className': 'file-info icon-text'}, DOM.create_element('span', {'className': 'icon-text__text'}, 'Test test'), DOM.create_element('svg', {'className': 'icon'}, DOM.create_element('use', {'xlink:href': '#icon-test'}))))), '<a><span class="file-info icon-text"><span class="icon-text__text">Test test</span><svg class="icon"><use xlink:href="#icon-test"></use></svg></span></a>')

    def test_create_element_none(self):
        self.assertEqual(DOM.render(DOM.create_element('a', {}, None, DOM.create_element('span', {}, 'Test test'))), '<a><span>Test test</span></a>')

    def test_create_element_entity(self):
        self.assertEqual(DOM.render(DOM.create_element(Icon, {'name': 'rocket'})), '<svg class="icon"><use xlink:href="icon-rocket"></use></svg>')

    def test_create_document_fragment(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_document_fragment()), 'fragment')

    def test_create_text_node(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_text_node('Test text')), 'textnode')
        self.assertEqual(DOM.get_text_content(DOM.create_text_node('Test text')), 'Test text')

    def test_parse_html(self):
        self.assertEqual(DOM.render(DOM.parse_html('<p><span>Test text</span></p>')), '<p><span>Test text</span></p>')

    def test_append_child(self):
        parent = DOM.create_element('p')
        DOM.append_child(parent, DOM.create_element('span', {}, 'Test text'))
        self.assertEqual(DOM.render(parent), '<p><span>Test text</span></p>')

    def test_set_attribute(self):
        elt = DOM.create_element('a')
        DOM.set_attribute(elt, 'href', 'http://example.com')
        self.assertEqual(elt.get('href'), 'http://example.com')

    def test_get_tag_name(self):
        self.assertEqual(DOM.get_tag_name(DOM.create_element('p', {}, 'Test test')), 'p')

    def test_get_class_list(self):
        self.assertEqual(DOM.get_class_list(DOM.create_element('p', {'className': 'intro test'}, 'Test test')), ['intro', 'test'])

    def test_get_text_content(self):
        self.assertEqual(DOM.get_text_content(DOM.create_element('p', {}, 'Test test')), 'Test test')

    def test_set_text_content(self):
        elt = DOM.create_element('p')
        DOM.set_text_content(elt, 'Test test')
        self.assertEqual(DOM.get_text_content(elt), 'Test test')

    def test_get_children(self):
        self.assertEqual(len(DOM.get_children(DOM.create_element('span', {}, DOM.create_element('span'), DOM.create_element('span')))), 2)

    def test_render(self):
        self.assertEqual(DOM.render(DOM.create_element('a', {}, DOM.create_element('span', {'className': 'file-info icon-text'}, DOM.create_element('span', {'className': 'icon-text__text'}, 'Test test'), DOM.create_element('svg', {'className': 'icon'}, DOM.create_element('use', {'xlink:href': '#icon-test'}))))), '<a><span class="file-info icon-text"><span class="icon-text__text">Test test</span><svg class="icon"><use xlink:href="#icon-test"></use></svg></span></a>')

    def test_pretty_print(self):
        self.assertEqual(DOM.pretty_print('<a><span class="file-info icon-text"><span class="icon-text__text">Test test</span><svg class="icon"><use xlink:href="#icon-test"></use></svg></span></a>'), '<a>\n   <span class="file-info icon-text">\n    <span class="icon-text__text">\n     Test test\n    </span>\n    <svg class="icon">\n     <use xlink:href="#icon-test">\n     </use>\n    </svg>\n   </span>\n  </a>')
