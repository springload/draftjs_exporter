from __future__ import absolute_import, unicode_literals

import re

# Python 2/3 unicode compatibility hack.
# See http://stackoverflow.com/questions/6812031/how-to-make-unicode-string-with-python3
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    def unicode(s):
        return str(s)

# BeautifulSoup import and helpers.
try:
    from bs4 import BeautifulSoup

    # Cache empty soup so we can create tags in isolation without the performance overhead.
    soup = BeautifulSoup('', 'html5lib')
except ImportError:
    pass


# lxml import and helpers.
try:
    from lxml import etree, html

    NSMAP = {
        'xlink': 'http://www.w3.org/1999/xlink',
    }
except ImportError:
    pass


class DOMEngine(object):
    """
    Parent class of all DOM implementations.
    """

    @staticmethod
    def create_tag(type_, attr=None):
        raise NotImplementedError

    @staticmethod
    def parse_html(markup):
        raise NotImplementedError

    @staticmethod
    def append_child(elt, child):
        raise NotImplementedError

    @staticmethod
    def render(elt):
        raise NotImplementedError

    @staticmethod
    def render_debug(elt):
        raise NotImplementedError


class DOM_BS(DOMEngine):
    """
    BeautifulSoup + html5lib implementation of the DOM API.
    """

    @staticmethod
    def create_tag(type_, attr=None):
        if not attr:
            attr = {}

        return soup.new_tag(type_, **attr)

    @staticmethod
    def parse_html(markup):
        return BeautifulSoup(markup, 'html5lib')

    @staticmethod
    def append_child(elt, child):
        elt.append(child)

    @staticmethod
    def render(elt):
        return re.sub(r'</?(fragment|body|html|head)>', '', unicode(elt))

    @staticmethod
    def render_debug(elt):
        return re.sub(r'</?(body|html|head)>', '', unicode(elt))


class DOM_LXML(DOMEngine):
    """
    lxml implementation of the DOM API.
    """
    @staticmethod
    def create_tag(type_, attr=None):
        nsmap = None

        if attr:
            if 'xlink:href' in attr:
                attr['{%s}href' % NSMAP['xlink']] = attr.pop('xlink:href')
                nsmap = NSMAP

        return etree.Element(type_, attrib=attr, nsmap=nsmap)

    @staticmethod
    def parse_html(markup):
        return html.fromstring(markup)

    @staticmethod
    def append_child(elt, child):
        if hasattr(child, 'tag'):
            elt.append(child)
        else:
            c = etree.Element('fragment')
            c.text = child
            elt.append(c)

    @staticmethod
    def render(elt):
        return re.sub(r'</?fragment>', '', etree.tostring(elt, method='html', encoding='unicode'))

    @staticmethod
    def render_debug(elt):
        return etree.tostring(elt, method='html', encoding='unicode')
