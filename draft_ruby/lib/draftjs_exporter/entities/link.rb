# frozen_string_literal: true
module DraftjsExporter
  module Entities
    class Link
      def call(parent_element, data)
        element = parent_element.document.create_element('a', href: data.fetch(:data, {}).fetch(:url))
        parent_element.add_child(element)
        element
      end
    end
  end
end
