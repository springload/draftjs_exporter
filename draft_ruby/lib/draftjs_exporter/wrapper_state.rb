module DraftjsExporter
  class WrapperState
    def initialize(block_map)
      @block_map = block_map
      @document = Nokogiri::HTML::Document.new
      @fragment = Nokogiri::HTML::DocumentFragment.new(document)
      reset_wrapper
    end

    def element_for(block)
      type = block.fetch(:type, 'unstyled')
      document.create_element(block_options(type)).tap do |e|
        parent_for(type).add_child(e)
      end
    end

    def to_s
      fragment.to_s
    end

    private

    attr_reader :fragment, :document, :block_map, :wrapper

    def set_wrapper(element, options = {})
      @wrapper = [element, options]
    end

    def wrapper_element
      @wrapper[0] || fragment
    end

    def wrapper_options
      @wrapper[1]
    end

    def parent_for(type)
      options = block_map.fetch(type)
      return reset_wrapper unless options.key?(:wrapper)

      new_options = nokogiri_options(*options.fetch(:wrapper))
      return wrapper_element if new_options == wrapper_options

      create_wrapper(new_options)
    end

    def reset_wrapper
      set_wrapper(fragment)
      wrapper_element
    end

    def nokogiri_options(element_name, element_attributes)
      config = element_attributes || {}
      options = {}
      options[:class] = config.fetch(:className) if config.key?(:className)
      [element_name, options]
    end

    def block_options(type)
      block_map.fetch(type).fetch(:element)
    end

    def create_wrapper(options)
      document.create_element(*options).tap do |new_element|
        reset_wrapper.add_child(new_element)
        set_wrapper(new_element, options)
      end
    end
  end
end
