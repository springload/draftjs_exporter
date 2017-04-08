from __future__ import absolute_import, unicode_literals

from draftjs_exporter.error import ExporterException


class ConfigException(ExporterException):
    pass


class Options:
    """
    Facilitates querying data from a config map.
    """
    def __init__(self, type_, element, props=None, wrapper=None, wrapper_props=None):
        self.type = type_
        self.element = element
        self.props = props if props else {}
        self.wrapper = wrapper
        self.wrapper_props = wrapper_props

    def __str__(self):
        return '<Options {0} {1} {2} {3} {4}>'.format(self.type, self.element, self.props, self.wrapper, self.wrapper_props)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    @staticmethod
    def for_block(block_map, type_):
        if type_ not in block_map:
            raise ConfigException('Block "%s" does not exist in block_map' % type_)

        block = block_map.get(type_)

        if isinstance(block, list):
            raise ConfigException('Block "%s" uses unsupported list-style config' % type_)
        elif isinstance(block, dict):
            if 'element' not in block:
                raise ConfigException('Block "%s" does not define an element' % type_)

            opts = Options(type_, **block)
        else:
            opts = Options(type_, block)

        return opts

    @staticmethod
    def for_style(style_map, type_):
        if type_ not in style_map:
            raise ConfigException('Style "%s" does not exist in style_map' % type_)

        style = style_map.get(type_)

        if isinstance(style, dict):
            if 'element' not in style:
                raise ConfigException('Style "%s" does not define an element' % type_)

            opts = Options(type_, **style)
        else:
            opts = Options(type_, style)

        return opts
