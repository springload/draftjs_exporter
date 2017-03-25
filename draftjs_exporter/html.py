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
        self.document = DOM.create_document_fragment()
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks', []):
            depth = block['depth']
            elt = self.render_block(block, entity_map)

            # At level 0, the element is added to the document.
            if depth == 0:
                DOM.append_child(self.document, elt)

        """
        Special method to handle a rare corner case: if there is no block
        at depth 0, we need to add the wrapper that contains the whole
        tree to the document.
        """
        document_length = len(DOM.get_children(self.document))

        if document_length == 0 and self.wrapper_state.stack.length() != 0:
            DOM.append_child(self.document, self.wrapper_state.stack.tail().elt)

        return DOM.render(self.document)

    def render_block(self, block, entity_map):
        content = DOM.create_document_fragment()
        entity_state = EntityState(self.entity_decorators, entity_map)
        style_state = StyleState(self.style_map)

        for (text, commands) in self.build_command_groups(block):
            for command in commands:
                entity_state.apply(command)
                style_state.apply(command)

            # Decorators are not rendered inside entities.
            if entity_state.has_no_entity() and len(self.composite_decorators) > 0:
                decorated_node = render_decorators(self.composite_decorators, text, block.get('type', None))
            else:
                decorated_node = DOM.create_text_node(text)

            styled_node = style_state.render_styles(decorated_node)
            entity_node = entity_state.render_entitities(styled_node)
            if entity_node:
                DOM.append_child(content, entity_node)
                DOM.append_child(content, styled_node)

        return self.wrapper_state.element_for(block, content)

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
            else:
                sliced.append((text[start_index:start_index], list(commands)))
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
