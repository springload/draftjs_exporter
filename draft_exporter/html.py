from .wrapper_state import WrapperState


class HTML():
    def __init__(self, config):
        self.block_map = config.get('block_map', {})
        self.style_map = config.get('style_map', {})
        self.entity_decorators = config.get('entity_decorators', {})

        self.wrapper_state = WrapperState(self.block_map)
        # self.style_state = StyleState(self.style_map)

    def call(self, content_state):
        entity_map = content_state.get('entityMap', {})

        for block in content_state.get('blocks'):
            element = self.wrapper_state.element_for(block)
            self.block_contents(element, block, entity_map)

        # Debugging command
        # wrapper_state.to_browser()

        return self.wrapper_state.to_string()

    def block_contents(self, element, block, entity_map):
        # entity_state = EntityState.new(element, entity_decorators, entity_map)
        # build_command_groups(block).each do |text, commands|
        # commands.each do |command|
        #   entity_state.apply(command)
        #   style_state.apply(command)
        # end

        # add_node(entity_state.current_parent, text, style_state)
        # end
        pass
