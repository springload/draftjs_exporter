# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest

from draftjs_exporter.dom_engine import DOM_HTML5LIB, DOM_LXML, DOMEngine


class TestDOMEngine(unittest.TestCase):
    def test_create_tag(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.create_tag(None)

    def test_parse_html(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.parse_html(None)

    def test_append_child(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.append_child(None, None)

    def test_render(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.render(None)

    def test_render_debug(self):
        with self.assertRaises(NotImplementedError):
            DOMEngine.render_debug(None)


class TestDOM_HTML5LIB(unittest.TestCase):
    def test_create_tag(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_create_tag_empty(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.create_tag('p')), '<p></p>')

    def test_parse_html(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.parse_html('<p><span>Test text</span></p>')), '<p><span>Test text</span></p>')

    def test_append_child(self):
        parent = DOM_HTML5LIB.create_tag('p')
        DOM_HTML5LIB.append_child(parent, DOM_HTML5LIB.create_tag('span', {}))
        self.assertEqual(DOM_HTML5LIB.render_debug(parent), '<p><span></span></p>')

    def test_render(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_render_debug(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')


class TestDOM_LXML(unittest.TestCase):
    def test_create_tag(self):
        self.assertEqual(DOM_LXML.render_debug(DOM_LXML.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_create_tag_empty(self):
        self.assertEqual(DOM_LXML.render_debug(DOM_LXML.create_tag('p')), '<p></p>')

    def test_parse_html(self):
        self.assertEqual(DOM_LXML.render_debug(DOM_LXML.parse_html('<p><span>Test text</span></p>')), '<p><span>Test text</span></p>')

    def test_append_child(self):
        parent = DOM_LXML.create_tag('p')
        DOM_LXML.append_child(parent, DOM_LXML.create_tag('span', {}))
        self.assertEqual(DOM_LXML.render_debug(parent), '<p><span></span></p>')

    def test_render(self):
        self.assertEqual(DOM_LXML.render_debug(DOM_LXML.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')

    def test_render_debug(self):
        self.assertEqual(DOM_LXML.render_debug(DOM_LXML.create_tag('p', {'class': 'intro'})), '<p class="intro"></p>')


class TestDOM_HTML5LIB_LXML_Differences(unittest.TestCase):
    def test_html5lib_self_closing_tags(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.create_tag('hr')), '<hr/>')

    def test_lxml_self_closing_tags(self):
        self.assertEqual(DOM_LXML.render_debug(DOM_LXML.create_tag('hr')), '<hr>')

    def test_html5lib_invalid_attributes(self):
        self.assertEqual(DOM_HTML5LIB.render_debug(DOM_HTML5LIB.create_tag('div', {'*ngFor': 'test'})), '<div *ngFor="test"></div>')

    def test_lxml_invalid_attributes(self):
        with self.assertRaises(ValueError):
            DOM_LXML.render_debug(DOM_LXML.create_tag('div', {'*ngFor': 'test'}))

    def test_html5lib_namespaced_attributes(self):
        bs_elt = DOM_HTML5LIB.create_tag('svg')
        DOM_HTML5LIB.append_child(bs_elt, DOM_HTML5LIB.create_tag('use', {'xlink:href': 'test'}))
        self.assertEqual(DOM_HTML5LIB.render_debug(bs_elt), '<svg><use xlink:href="test"></use></svg>')

    def test_lxml_namespaced_attributes(self):
        lxml_elt = DOM_LXML.create_tag('svg')
        DOM_LXML.append_child(lxml_elt, DOM_LXML.create_tag('use', {'xlink:href': 'test'}))
        self.assertEqual(DOM_LXML.render_debug(lxml_elt), '<svg><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="test"></use></svg>')
