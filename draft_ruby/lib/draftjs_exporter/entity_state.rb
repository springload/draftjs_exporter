# frozen_string_literal: true
require 'draftjs_exporter/entities/null'
require 'draftjs_exporter/error'

module DraftjsExporter
  class InvalidEntity < DraftjsExporter::Error; end

  class EntityState
    attr_reader :entity_decorators, :entity_map, :entity_stack, :root_element

    def initialize(root_element, entity_decorators, entity_map)
      @entity_decorators = entity_decorators
      @entity_map = entity_map
      @entity_stack = [[Entities::Null.new.call(root_element, nil), nil]]
    end

    def apply(command)
      case command.name
      when :start_entity
        start_command(command)
      when :stop_entity
        stop_command(command)
      end
    end

    def current_parent
      element, _data = entity_stack.last
      element
    end

    private

    def start_command(command)
      entity_details = entity_map.fetch(command.data.to_s)
      decorator = entity_decorators.fetch(entity_details.fetch(:type))
      parent_element = entity_stack.last.first
      new_element = decorator.call(parent_element, entity_details)
      entity_stack.push([new_element, entity_details])
    end

    def stop_command(command)
      entity_details = entity_map.fetch(command.data.to_s)
      _element, expected_entity_details = entity_stack.last

      if expected_entity_details != entity_details
        raise InvalidEntity, "Expected #{expected_entity_details.inspect} got #{entity_details.inspect}"
      end

      entity_stack.pop
    end
  end
end
