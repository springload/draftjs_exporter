from __future__ import absolute_import, unicode_literals

import inspect
import re

from draftjs_exporter.error import ConfigException

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

    def Soup(raw_str):
        """
        Wrapper around BeautifulSoup to keep the code DRY.
        """
        return BeautifulSoup(raw_str, 'html5lib')

    # Cache empty soup so we can create tags in isolation without the performance overhead.
    soup = Soup('')
except ImportError:
    pass

# LXML import and helpers.
try:
    from lxml import etree, html

    NSMAP = {
        'xlink': 'http://www.w3.org/1999/xlink',
    }
except ImportError:
    pass


class DOMEngine(object):
    @staticmethod
    def create_tag(type_, attr=None):
        raise NotImplementedError()

    @staticmethod
    def parse_html(markup):
        raise NotImplementedError()

    @staticmethod
    def append_child(elt, child):
        raise NotImplementedError()

    @staticmethod
    def render(elt):
        raise NotImplementedError()

    @staticmethod
    def render_debug(elt):
        raise NotImplementedError()


class DOM_BS(DOMEngine):
    @staticmethod
    def create_tag(type_, attr=None):
        if not attr:
            attr = {}

        return soup.new_tag(type_, **attr)

    @staticmethod
    def parse_html(markup):
        return Soup(markup)

    @staticmethod
    def append_child(elt, child):
        elt.append(child)

    @staticmethod
    def render(elt):
        return re.sub(r'</?(fragment|body|html|head)>', '', unicode(elt)).strip()

    @staticmethod
    def render_debug(elt):
        return re.sub(r'</?(body|html|head)>', '', unicode(elt)).strip()


class DOM_LXML(DOMEngine):
    """
    Wrapper around our HTML building library to facilitate changes.
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
        return re.sub(r'(</?(fragment)>|xmlns:xlink="http://www.w3.org/1999/xlink" )', '', etree.tostring(elt, method='html', encoding='unicode'))

    @staticmethod
    def render_debug(elt):
        return re.sub(r'(xmlns:xlink="http://www.w3.org/1999/xlink" )', '', etree.tostring(elt, method='html', encoding='unicode'))


# https://gist.github.com/yahyaKacem/8170675
_first_cap_re = re.compile(r'(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


class DOM(object):
    BS = 'bs'
    LXML = 'lxml'

    dom = DOM_BS

    @staticmethod
    def camel_to_dash(camel_cased_str):
        sub2 = _first_cap_re.sub(r'\1-\2', camel_cased_str)
        dashed_case_str = _all_cap_re.sub(r'\1-\2', sub2).lower()
        return dashed_case_str.replace('--', '-')

    @classmethod
    def use(cls, engine=DOM_BS):
        """
        Configure the DOM implementation.
        """
        if engine:
            if inspect.isclass(engine):
                cls.dom = engine
            elif engine.lower() == cls.BS:
                cls.dom = DOM_BS
            elif engine.lower() == cls.LXML:
                cls.dom = DOM_LXML
            else:
                raise ConfigException('Invalid DOM engine.')

    @classmethod
    def create_element(cls, type_=None, props=None, *children):
        """
        Signature inspired by React.createElement.
        createElement(
          string/ReactClass type,
          [object props],
          [children ...]
        )
        https://facebook.github.io/react/docs/top-level-api.html#react.createelement
        """
        if props is None:
            props = {}

        if not type_:
            return cls.create_tag('fragment')
        else:
            if len(children) and isinstance(children[0], (list, tuple)):
                children = children[0]

            if inspect.isclass(type_):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_().render(props)
            elif callable(getattr(type_, 'render', None)):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_.render(props)
            elif callable(type_):
                props['children'] = children[0] if len(children) == 1 else children
                elt = type_(props)
            else:
                # Never render those attributes on a raw tag.
                props.pop('children', None)
                props.pop('block', None)

                if 'style' in props and isinstance(props['style'], dict):
                    rules = ['{0}: {1};'.format(DOM.camel_to_dash(s), props['style'][s]) for s in props['style'].keys()]
                    props['style'] = ''.join(sorted(rules))

                # Map props from React/Draft.js to HTML lingo.
                if 'className' in props:
                    props['class'] = props.pop('className')

                attributes = {}
                for key in props:
                    if props[key] is False:
                        props[key] = 'false'

                    if props[key] is True:
                        props[key] = 'true'

                    if props[key] is not None:
                        attributes[key] = unicode(props[key])

                elt = cls.create_tag(type_, attributes)

                for child in children:
                    if child not in (None, ''):
                        cls.append_child(elt, child)
        return elt

    @classmethod
    def create_tag(cls, type_, props=None):
        return cls.dom.create_tag(type_, props)

    @classmethod
    def parse_html(cls, markup):
        return cls.dom.parse_html(markup)

    @classmethod
    def append_child(cls, elt, child):
        return cls.dom.append_child(elt, child)

    @classmethod
    def render(cls, elt):
        return cls.dom.render(elt)

    @classmethod
    def render_debug(cls, elt):
        return cls.dom.render_debug(elt)
