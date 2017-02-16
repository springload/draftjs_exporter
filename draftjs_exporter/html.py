from __future__ import absolute_import, unicode_literals

from itertools import groupby

from draftjs_exporter.command import Command
from draftjs_exporter.composite_decorators import render_decorators
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.dom import DOM
from draftjs_exporter.entity_state import EntityState
from draftjs_exporter.style_state import StyleState
from draftjs_exporter.wrapper_state import WrapperState


class HTML:
    """
    Entry point of the exporter. Combines entity, wrapper and style state
    to generate the right HTML nodes.
    """
    def __init__(self, config=None):
        if config is None:
            config = {}

        self.entity_decorators = config.get('entity_decorators', {})
        self.composite_decorators = config.get('composite_decorators', [])
        self.block_map = config.get('block_map', BLOCK_MAP)
        self.style_map = config.get('style_map', STYLE_MAP)

    def render(self, content_state):
        """
        Starts the export process on a given piece of content state.
        """
        self.wrapper_state = WrapperState(self.block_map)
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks', []):
            self.render_block(block, entity_map)

        self.wrapper_state.clean_up()

        return self.wrapper_state.to_string()

    def render_block(self, block, entity_map):
        element = self.wrapper_state.element_for(block)
        entity_state = EntityState(self.entity_decorators, entity_map)
        style_state = StyleState(self.style_map)

        for (text, commands) in self.build_command_groups(block):
            for command in commands:
                entity_state.apply(command)
                style_state.apply(command)

            # Decorators are not rendered inside entities.
            if entity_state.is_empty() and len(self.composite_decorators) > 0:
                decorated_node = render_decorators(self.composite_decorators, text, block.get('type', None))
            else:
                decorated_node = DOM.create_text_node(text)

            styled_node = style_state.render_styles(decorated_node)
            entity_state.render_entitities(element, styled_node)

    def build_command_groups(self, block):
        """
        Creates block modification commands, grouped by start index,
        with the text to apply them on.
        """
        text = block.get('text')

        commands = sorted(self.build_commands(block))
        grouped = groupby(commands, Command.key)
        listed = list(groupby(commands, Command.key))
        sliced = []

        i = 0
        for start_index, commands in grouped:
            if i < len(listed) - 1:
                stop_index = listed[i + 1][0]
                sliced.append((text[start_index:stop_index], list(commands)))
            i += 1

        return sliced

    def build_commands(self, block):
        """
        Build all of the manipulation commands for a given block.
        - One pair to set the text.
        - Multiple pairs for styles.
        - Multiple pairs for entities.
        """
        text_commands = Command.start_stop('text', 0, len(block.get('text')))
        style_commands = self.build_style_commands(block)
        entity_commands = self.build_entity_commands(block)

        return text_commands + style_commands + entity_commands

    def build_style_commands(self, block):
        ranges = block.get('inlineStyleRanges', [])
        return Command.from_ranges(ranges, 'inline_style', 'style')

    def build_entity_commands(self, block):
        ranges = block.get('entityRanges', [])
        return Command.from_ranges(ranges, 'entity', 'key')
