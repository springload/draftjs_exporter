from lxml import etree

from .command import Command
from .entity_state import EntityState
from .style_state import StyleState
from .wrapper_state import WrapperState


class HTML():
    def __init__(self, config):
        self.block_map = config.get('block_map', {})
        self.style_map = config.get('style_map', {})
        self.entity_decorators = config.get('entity_decorators', {})

        self.wrapper_state = WrapperState(self.block_map)

    def call(self, content_state):
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks'):
            element = self.wrapper_state.element_for(block)
            self.block_contents(element, block, entity_map)

        return self.wrapper_state.to_string()

    def block_contents(self, element, block, entity_map):
        style_state = StyleState(self.style_map)
        entity_state = EntityState(element, self.entity_decorators, entity_map)
        for (text, commands) in self.build_command_groups(block):
            for command in commands:
                entity_state.apply(command)
                style_state.apply(command)

            # TODO Use entity_state.
            self.add_node(element, text, style_state)

    def add_node(self, element, text, style_state):
        if style_state.is_unstyled():
            child = etree.SubElement(element, 'textnode')
            child.text = text
        else:
            child = etree.SubElement(element, 'span', attrib=style_state.element_attributes())
            child.text = text
        # document = element.getroot()
        # node = if state.text?
        # document.create_text_node(text)
        # else
        # document.create_element('span', text, state.element_attributes)
        # end
        # element.add_child(node)

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
