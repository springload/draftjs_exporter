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
            self.start_command(command)
        elif command.name == 'stop_entity':
            self.stop_command(command)

    def has_no_entity(self):
        return not self.entity_stack

    def get_entity_details(self, command):
        key = str(command.data)
        details = self.entity_map.get(key)

        if details is None:
            raise EntityException('Entity "%s" does not exist in the entityMap' % key)

        return details

    def get_entity_decorator(self, entity_details):
        type_ = entity_details.get('type')

        if type_ not in self.entity_decorators:
            raise EntityException('Decorator "%s" does not exist in entity_decorators' % type_)

        decorator = self.entity_decorators.get(type_)

        return decorator

    def start_command(self, command):
        entity_details = self.get_entity_details(command)
        self.entity_stack.append(entity_details)

    def stop_command(self, command):
        entity_details = self.get_entity_details(command)
        expected_entity_details = self.entity_stack[-1]

        if expected_entity_details != entity_details:
            raise EntityException('Expected {0}, got {1}'.format(expected_entity_details, entity_details))

        self.completed_entity = self.entity_stack.pop()

    def render_entitities(self, style_node):

        if self.completed_entity:
            # self.element_stack.append(style_node)
            decorator = self.get_entity_decorator(self.completed_entity)
            props = self.completed_entity.get('data').copy()

            nodes = DOM.create_document_fragment()
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
