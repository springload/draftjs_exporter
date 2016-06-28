from .wrapper_state import WrapperState


class HTML():
    def __init__(self, config):
        self.block_map = config.get('block_map')
        self.style_map = config.get('style_map')
        self.entity_decorators = config.get('entity_decorators')

    def call(self, content_state):
        wrapper_state = WrapperState(self.block_map)

        for block in content_state.get('blocks'):
            wrapper_state.element_for(block)

        # Debugging command
        # wrapper_state.to_browser()

        return wrapper_state.to_string()
