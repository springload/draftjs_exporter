

class EntityState():
    def __init__(self, element, entity_decorators, entity_map):
        self.styles = []
        self.entity_decorators = entity_decorators
        self.entity_map = entity_map
        self.entity_stack = []

    def apply(self, command):
        pass
