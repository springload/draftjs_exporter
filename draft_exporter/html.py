from itertools import groupby
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
                print text, command
                entity_state.apply(command)
                style_state.apply(command)

            # add_node(entity_state.current_parent, text, style_state)

    def build_command_groups(self, block):
        text = block.get('text')
        commands = self.build_commands(block)
        # grouped = build_commands(block).group_by(&:index).sort
        # grouped = sorted(list(groupby(commands, lambda c: c.index)))
        grouped = groupby(commands, lambda c: c.index)
        listed = list(groupby(commands, lambda c: c.index))

        grouped_sliced = []
        i = 0
        for start_index, commands in grouped:
            next_group = listed[i + 1] if i + 1 < len(listed) else False
            # TODO stop_index should be set depending on the languages' slice implementation.
            # stop_index = (next_group && next_group.first || 0) - 1
            # [text.slice(start_index..stop_index), commands]
            stop_index = next_group[0] if next_group else - 1

            grouped_sliced.append((text[start_index:stop_index], list(commands)))
            i += 1

        return grouped_sliced

    def build_commands(self, block):
        return [
            Command('start_text', 0),
            Command('stop_text', len(block.get('text'))),
        ]
        # TODO Add additional commands
        # build_range_commands(:inline_style, :style, block.fetch(:inlineStyleRanges)) +
        # build_range_commands(:entity, :key, block.fetch(:entityRanges))

    def build_range_commands(self, name, data_key, ranges):
        pass
        # ranges.flat_map { |range|
        #     data = range.get(data_key)
        #     start = range.get('offset')
        #     stop = start + range.get('length')
        #     [
        #         Command.new('start_#{name}'.to_sym, start, data),
        #         Command.new('stop_#{name}'.to_sym, stop, data)
        #     ]
        # }
