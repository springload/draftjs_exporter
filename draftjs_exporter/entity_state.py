from __future__ import absolute_import, unicode_literals

from draftjs_exporter.dom import DOM
from draftjs_exporter.error import ExporterException


class EntityException(ExporterException):
    pass


class EntityState:
    def __init__(self, entity_decorators, entity_map):
        self.entity_decorators = entity_decorators
        self.entity_map = entity_map

        self.entity_stack = []
        self.completed_entity = None
        self.element_stack = []

    def apply(self, command):
        if command.name == 'start_entity':
            self.entity_stack.append(command.data)
        elif command.name == 'stop_entity':
            expected_entity = self.entity_stack[-1]

            if command.data != expected_entity:
                raise EntityException('Expected {0}, got {1}'.format(expected_entity, command.data))

            self.completed_entity = self.entity_stack.pop()

    def has_no_entity(self):
        return not self.entity_stack

    def get_entity_details(self, entity_key):
        details = self.entity_map.get(str(entity_key))

        if details is None:
            raise EntityException('Entity "%s" does not exist in the entityMap' % entity_key)

        return details

    def get_entity_decorator(self, type_):
        if type_ not in self.entity_decorators:
            raise EntityException('Decorator "%s" does not exist in entity_decorators' % type_)

        decorator = self.entity_decorators[type_]

        return decorator

    def render_entitities(self, style_node):

        if self.completed_entity is not None:
            # self.element_stack.append(style_node)
            entity_details = self.get_entity_details(self.completed_entity)
            decorator = self.get_entity_decorator(entity_details['type'])
            props = entity_details['data'].copy()

            nodes = DOM.create_element()

            for n in self.element_stack:
                DOM.append_child(nodes, n)

            elt = DOM.create_element(decorator, props, nodes)

            self.completed_entity = None
            self.element_stack = []
        elif self.has_no_entity():
            elt = style_node
        else:
            self.element_stack.append(style_node)
            elt = None

        return elt
