from __future__ import absolute_import, unicode_literals

from draftjs_exporter.constants import BLOCK_TYPES, ENTITY_TYPES, INLINE_STYLES
from draftjs_exporter.error import ConfigException


class Options:
    """
    Facilitates querying configuration from a config map.
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
    def for_kind(kind_map, type_, fallback_key):
        """
        Create an Options object from any mapping.
        """
        if type_ not in kind_map:
            if fallback_key not in kind_map:
                raise ConfigException('"%s" is not in the config and has no fallback' % type_)

            config = kind_map[fallback_key]
        else:
            config = kind_map[type_]

        if isinstance(config, dict):
            if 'element' not in config:
                raise ConfigException('"%s" does not define an element' % type_)

            opts = Options(type_, **config)
        else:
            opts = Options(type_, config)

        return opts

    @staticmethod
    def for_block(block_map, type_):
        return Options.for_kind(block_map, type_, BLOCK_TYPES.FALLBACK)

    @staticmethod
    def for_style(style_map, type_):
        return Options.for_kind(style_map, type_, INLINE_STYLES.FALLBACK)

    @staticmethod
    def for_entity(entity_map, type_):
        return Options.for_kind(entity_map, type_, ENTITY_TYPES.FALLBACK)
