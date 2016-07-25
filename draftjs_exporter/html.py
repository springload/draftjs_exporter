from __future__ import absolute_import, unicode_literals

from draftjs_exporter.command import Command
from draftjs_exporter.defaults import BLOCK_MAP, STYLE_MAP
from draftjs_exporter.entity_state import EntityState
from draftjs_exporter.style_state import StyleState
from draftjs_exporter.wrapper_state import WrapperState


class HTML():
    """
    Entry point of the exporter. Combines entity, wrapper and style state
    to generate the right HTML nodes.
    """
    def __init__(self, config={}):
        self.entity_decorators = config.get('entity_decorators', {})
        self.wrapper_state = WrapperState(config.get('block_map', BLOCK_MAP))
        self.style_state = StyleState(config.get('style_map', STYLE_MAP))

    def render(self, content_state):
        """
        Starts the export process on a given piece of content state.
        """
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks', []):
            self.render_block(block, entity_map)

        return self.wrapper_state.to_string()

    def render_block(self, block, entity_map):
        element = self.wrapper_state.element_for(block)
        entity_state = EntityState(element, self.entity_decorators, entity_map)

        for (text, commands) in self.build_command_groups(block):
            for command in commands:
                entity_state.apply(command)
                self.style_state.apply(command)

            self.style_state.add_node(entity_state.current_parent(), text)

    def build_command_groups(self, block):
        """
        Creates block modification commands, grouped by start index,
        with the text to apply them on.
        """
        text = block.get('text')

        commands = self.build_commands(block)
        # Tried using itertools.tee but for some reason that failed. Oh well.
        grouped = Command.grouped_by_index(commands)
        listed = list(Command.grouped_by_index(commands))
        sliced = []

        i = 0
        for start_index, commands in grouped:
            next_group = listed[i + 1] if i + 1 < len(listed) else False
            stop_index = next_group[0] if next_group else 0

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
