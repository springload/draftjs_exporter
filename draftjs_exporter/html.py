from __future__ import absolute_import, unicode_literals

from .command import Command
from .entity_state import EntityState
from .style_state import StyleState
from .wrapper_state import WrapperState


class HTML():
    """
    Entry point of the exporter. Combines entity, wrapper and style state
    to generate the right HTML nodes.
    """
    def __init__(self, config):
        self.entity_decorators = config.get('entity_decorators', {})
        self.wrapper_state = WrapperState(config.get('block_map', {}))
        self.style_state = StyleState(config.get('style_map', {}))

    def call(self, content_state):
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks'):
            element = self.wrapper_state.element_for(block)
            self.render_block(element, block, entity_map)

        return self.wrapper_state.to_string()

    def render_block(self, element, block, entity_map):
        entity_state = EntityState(element, self.entity_decorators, entity_map)
        for (text, commands) in self.build_command_groups(block):
            for command in commands:
                entity_state.apply(command)
                self.style_state.apply(command)

            self.style_state.add_node(entity_state.current_parent(), text)

    def build_command_groups(self, block):
        """
        Creates block modification commands, grouped by start index, with the text to apply them on.
        """
        commands = self.build_commands(block)
        # TODO Tried using itertools.tee but for some reason that does not work. Oh well.
        grouped = Command.grouped_by_index(commands)
        listed = list(Command.grouped_by_index(commands))

        text = block.get('text')
        grouped_sliced = []
        i = 0
        for start_index, commands in grouped:
            next_group = listed[i + 1] if i + 1 < len(listed) else False
            stop_index = next_group[0] if next_group else 0

            grouped_sliced.append((text[start_index:stop_index], list(commands)))
            i += 1

        return grouped_sliced

    def build_commands(self, block):
        text_commands = Command.start_stop('text', 0, len(block.get('text')))
        style_commands = self.build_style_commands(block)
        entity_commands = self.build_entity_commands(block)

        return text_commands + style_commands + entity_commands

    def build_style_commands(self, block):
        return Command.from_ranges(block.get('inlineStyleRanges', []), 'inline_style', 'style')

    def build_entity_commands(self, block):
        return Command.from_ranges(block.get('entityRanges', []), 'entity', 'key')
