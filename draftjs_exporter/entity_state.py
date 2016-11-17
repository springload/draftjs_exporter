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

    def apply(self, command):
        if command.name == 'start_entity':
            self.start_command(command)
        elif command.name == 'stop_entity':
            self.stop_command(command)

    def get_entity_details(self, command):
        key = str(command.data)
        details = self.entity_map.get(key)

        if details is None:
            raise EntityException('Entity "%s" does not exist in the entityMap' % key)

        return details

    def get_entity_decorator(self, entity_details):
        type_ = entity_details.get('type')
        decorator = self.entity_decorators.get(type_)

        if decorator is None:
            raise EntityException('Decorator "%s" does not exist in entity_decorators' % type_)

        return decorator

    def start_command(self, command):
        entity_details = self.get_entity_details(command)
        self.entity_stack.append(entity_details)

    def stop_command(self, command):
        entity_details = self.get_entity_details(command)
        expected_entity_details = self.entity_stack[-1]

        if expected_entity_details != entity_details:
            raise EntityException('Expected {0}, got {1}'.format(expected_entity_details, entity_details))

        self.entity_stack.pop()

    def render_entitities(self, root_element, style_node):
        stack_start = DOM.create_document_fragment()
        DOM.append_child(root_element, stack_start)

        element_stack = [stack_start]
        new_element = stack_start

        if len(self.entity_stack) == 0:
            DOM.append_child(root_element, style_node)
        else:
            for entity_details in self.entity_stack:
                decorator = self.get_entity_decorator(entity_details)

                entity_details['children'] = style_node

                new_element = decorator.render(entity_details)
                DOM.append_child(element_stack[-1], new_element)
                element_stack.append(new_element)

        return new_element
