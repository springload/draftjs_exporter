# frozen_string_literal: true
module DraftjsExporter
  module Entities
    class Null
      def call(parent_element, _data)
        parent_element
      end
    end
  end
end
